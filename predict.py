import re
import pandas as pd
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import sqlite3
import time
from datetime import datetime, timedelta


print('Predict Module Load')
# ler o ficheiro com as notícias classificadas
print('Predit - load Noticias')
df=pd.read_excel('FakeRecogna.xlsx', sheet_name = 'Sheet1')
# tratamento necessário
#    eliminar campos desnecessários do ficheiro, devido a ter > 50% de nulls
df.drop('Subtitulo', inplace=True, axis=1)

#    eliminar registos duplicados, com o mesmo título (validado que os restantes campos também estão duplicados) 
df = df.drop_duplicates("Titulo", keep='first')
df= df.reset_index(drop=True)

#    tratar da coluna "Autor" que tem valores null e muitos casos com a data da notícia (procurando 20 do ano 2000)
print('Predict - prepare Autor')
df["Autor"].fillna("none", inplace= True)
df.loc[df.Autor.str.contains("20"), "Autor"] = 'none'
df["Autor"] = df["Autor"].str.replace("\n", "")

#    opter o domínio do site
print('Predict - get dominios noticias reais')
for i in range(df.shape[0]):
    url = df.iloc[i,5]
    dominio = urlparse(url).netloc
    df.loc[i, "Dominio"] = dominio

#    Lista de sites confiáveis
array_fake = df[df.Classe == 0.0].Dominio.unique()
array_real = df[df.Classe == 1.0].Dominio.unique()

s_real = set(array_real)-set(array_fake)
df_dominio_real = pd.DataFrame({'dominio': data} for data in s_real)

#      adicionar à lista mais alguns sites confiáveis
data = ['www.folha.uol.com.br', 'www.metropoles.com', 'www.estadao.com.br','www.cnnbrasil.com.br',
        'www.bbc.com/portuguese','exame.com','oglobo.globo.com','www.globo.com', 'pt.euronews.com'] 
df2 = pd.DataFrame(data, columns = ['dominio'])
df_dominio_real = pd.concat([df_dominio_real, df2], ignore_index=True, axis=0) 

#   Lista de sites fake
print('Predict - get dominios noticias fake')
data = ['checamos.afp.com', 'projetocomprova.com.br', 'www.boatos.org', 'www.e-farsas.com'] 
df_dominio_fake = pd.DataFrame(data, columns = ['dominio'])



#    Lista de autores confiáveis
print('Predict - get autores confiáveis')
array_fake = df[df.Classe == 0.0].Autor.unique()
array_real = df[df.Classe == 1.0].Autor.unique()

s_real = set(array_real)-set(array_fake)
df_autor_real = pd.DataFrame({'autor': data} for data in s_real)

# Treinar o modelo
print('Predict - Preparar modelo')
target=df.Classe
#    Aplica o processo TF-IDF (Term Frequency Inverse Document Frequency) para obter uma matriz com a importancia das palavras
tfidf_vectorizer = TfidfVectorizer(max_df=0.7)
series_noticia   = df['Noticia']
tfidf_train      = tfidf_vectorizer.fit_transform(series_noticia) 

#    Aplica ao resultado o modelo passivo-agressivo para aprender com a matriz já criada com 50 epocs
print('Predict - treinar modelo')
modelo=PassiveAggressiveClassifier(max_iter=50)
modelo.fit(tfidf_train,target)

#   Libertar memória
print('Predict - libertar memória')
del df
del array_fake
del array_real
del s_real
del series_noticia
del tfidf_train
del target

def predict_response(msg):
    #Prever se a msg é fake ou real através do modelo treinado
    print('Predict - function = predict_response')
    noticia = pd.Series([msg])
    tfidf=tfidf_vectorizer.transform(noticia)
    res = modelo.predict(tfidf)
    return res[0] 


def valid_autor(autor):
    #caso o autor da notícia exista, valida se pertence a autores e renome, ou seja, que sejam confiáveis
    print('Predict - function = valid_autor')
    resposta = -1 # não sabe
    if (autor in df_autor_real) and (autor != ""):
        resposta = 1 # é confiável
    return resposta

def valid_dominio(url):
    #Valida se o domínio (base do url) pertence à lista de domínios confiáveis
    print('Predict - function = valid_dominio')
    resposta = -1 # não sabe
    if url != "":
        dominio = urlparse(url).netloc
        if dominio in df_dominio_real.values:
            resposta = 1 # é confiável
        elif dominio in df_dominio_fake.values:
            resposta = 0 # é fake
    return resposta

def valid_data(data):
    # Dado que as notícias usadas no modelo são de 2019 até 2021, valida se o ano >= 2019
    print('Predict - function = valid_data')
    resposta = -1 # não sabe
    if data != "":
        # procurar pelo ano yyyy
        p=re.search(r"\d{4}", data)
        if int(0 if p is None else p.start()) > 0:
            ano = data[p.start():p.start()+4]
            if ano >= '2019':
                resposta = 1 # data válida
            else:
                resposta = 0 # data inválida
    return resposta

def valid_text(msg):
    # Submete um texto (corpo da notícia ou o título) ao modelo de ML treinado
    print('Predict - function = valid_text')
    resposta = -1 # não sabe
    if (len(msg) > 50):  # comprimento mínimo para analisar um texto (textos muito pequenos são susceptiveis a maiores falsos resultados)
        resposta = predict_response(msg)

    return resposta

def valid_url(title, autor, data, body):
    #esta é a função central, onde tem toda as regras de validação dos conteúdos da notícia
    # Regras:
    #   Validar domínio do URL: (este passo é realizado logo à entrada, ainda antes de chamar esta função)
    #       Confiável -> return 1 -> Fim (noticia verdadeira)
    #       Desconhece -> return -1 -> Validar autor da notícia (da entrada nesta função)
    #   Validar autor da notícia:
    #       Confiável -> return 1 -> Fim (noticia verdadeira)
    #       Desconhece -> return -1 -> Validar data da notícia
    #   Validar data da notícia:
    #       Dt válida -> return 1 -> validar o corpo da notícia
    #       Dt inválida -> return 0 -> Fim (não pode avaliar noticia. Notícia anterior a 2019)
    #       Desconhece -> return -1 -> validar o corpo da notícia
    #   Validar o corpo da notícia:
    #       Fato -> return 1 -> Fim (noticia verdadeira)
    #       Fake -> return 0 -> Fim (notícia falsa)
    #       Inconclusivo -> return -1 -> Validar título da notícia
    #   Validar título da notícia:
    #       Fato -> return 1 -> Fim (noticia verdadeira)
    #       Fake -> return 0 -> Fim (noticia false)
    #       Inconclusivo -> return -1 -> Fim (sem conclusão)
    print('Predict - function = valid_url')

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time(valid_url) =", current_time)

    msg = ""
    predict = -1 # não sabe
    v_autor = valid_autor(autor)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time(valid_autor) =", current_time)

    if v_autor == 1:
        # autor credível
        msg = "Tudo me leva a crer que a notícia seja verdadeira, mas pode..."
    else:
        v_data =  valid_data(data)
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time(valir_data) =", current_time)

        if v_data == 0:
            # data antiga
            msg = "Infelizmente essa notícia já é antiga e não consigo validar, mas aconcelho a..."
        else:
            v_body = valid_text(body)

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time(valid body) =", current_time)

            if v_body == 1:
                # notícia credível
                msg = "A notícia parece ser de verdadeira, mas deverá ..."
            elif v_body == 0:
                # fake news
                msg = "Há fortes indícios que aponta para uma notícia falsa, mas deverá ..."
            else:
                v_title = valid_text(title)

                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time(valid title) =", current_time)

                if v_body == 1:
                    # notícia credível
                    msg = "A notícia tem todos os atributos para crer que seja verdadeira, o entanto ..."
                elif v_body == 0:
                    # fake news
                    msg = "Tudo leva a crer que a notícia seja falsa, no entanto recomendo ..."
                else:
                    # inconclusivo
                    msg = "A informação não permitiu perceber se é fake ou real. Aconselhos antes de compartilhar, que leia a notícia completa, analise se o conteúdo do texto está relatando um fato ou não, se tem autor/responsabilidade e a data na publicação."

    return msg

##########################################################
# funções que trabalham uma BD SQLite3 do próprio Heroku
##########################################################
def create_DB(db_file):
    conn = None
    conn = sqlite3.connect(db_file)
    return conn

def select_MSG(conn, session_id):
    cur = conn.cursor()
    cur.execute("SELECT session_id, msg FROM tasks WHERE session_id=?", (session_id,))
    msg = ""

    rows = cur.fetchall()

    for row in rows:
        print(row)
        msg = row[1]
    cur.close()
    return msg 

def create_task_table(conn):
    cur = conn.cursor()
    table = """CREATE TABLE IF NOT EXISTS tasks (
                session_id   TEXT PRIMARY KEY,
                msg TEXT    NULL
            ); """
    cur.execute(table)
    cur.close()

def insert_task_table(conn, session_id, msg):
    cur = conn.cursor()
    sql = """INSERT INTO tasks (session_id, msg)
             VALUES (?, ?)
        """
    params = (session_id, msg)
    cur.execute(sql, params)
    conn.commit()
    cur.close()

def update_task_table(conn, session_id, msg):
    cur = conn.cursor()
    sql = """REPLACE INTO tasks (session_id, msg)
             VALUES (?, ?)
        """
    params = (session_id, msg)
    cur.execute(sql, params)
    conn.commit()
    cur.close()

def delete_task_table(conn, session_id, msg):
    cur = conn.cursor()
    sql = """DELETE FROM tasks 
             WHERE session_id = ?
        """
    params = (session_id,)
    cur.execute(sql, params)
    conn.commit()
    cur.close()

def close_connection(conn):
    conn.close()

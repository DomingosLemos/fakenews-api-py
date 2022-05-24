# fakenews-api-py

## Descrição

Todo o código aqui apresentado serviu como parte integrante de um projeto final de curso ***Botcamp*** da [LetsBot](https://www.letsbot.com.br/). 

O tema do projeto consiste na criação de um chatbot de auxilio no combate às Fakenews, por forma a contribuir para esta causa.

Um dos muitos temas que o chatbot vai responder é a capacidade de avaliar se uma notícia é verdadeira ou falsa, recorrendo à Inteligência Artifical. É neste ponto que entra esta API, realizada em Python.

O projeto final vai ser tescriadotado em Dialogflow, que irá usar o webhook para detetar fakenews de forma inteligente, e é aqui que entra a API. 

## Objetivo

O desafio é criar uma API que seja chamada pelo chatbot para detectar se uma determinada notícia, dada por um URL, é verdadeira ou não.

Um segundo desafio é fazer o código e disponibilizar na cloud ser qualquer custo, até porque é um projeto académico. Para tal foram apenas usadas ferramentas open source, como será descrito mais à frente.

## Grupo de trabalho

O projeto é composto por 6 elementos

[Carolina Santos](https://www.linkedin.com/in/mariacarolinademelosantos/) PO / UX Writer /Curadoria <br>
[Adriana Melo](https://www.linkedin.com/in/adriana-poletimelo/) UX Writer <br>
[Andréa Araújo](www.linkedin.com/in/andrea-araujo-749b1960/) UX Research / UX Writer <br>
[Domingos Lemos](www.linkedin.com/in/domingos-lemos-51b71970/) Scrum Master / Desenvolvedor <br>
[Marconne Resende](www.linkedin.com/in/marconnebiblio/) UX Research <br>
[Pedro Edgar](https://www.linkedin.com/in/pedro-edgar-240780205/) Desenvolvedor / Curadoria <br>

E a nossa mentora de projeto: [Ariana de Souza](https://www.linkedin.com/in/arianesouza/) <br>


## Pressupostos/limitações

Esta API tem as seguintes limitações:
* Apenas está preparado para responder à língua pt-br
* O dataset usado para o modelo incluí seis categorias, mas as mais bem representadas são política e saúde
* Só aceita URL de sites de notícias em formato texto. (imagens, som e vídeos não estão contemplados)
* O Dialogflow como canal não permite entrada pelo user maior que 256 caracteres, por isso a única forma de validar uma notícia é por ULR
* O tempo de espera de resposta de uma chamada a API pelo Dialogflow é de 5 segundos. Para ler a notícia de um site é necessário aceder ao mesmo e verificámos que alguns tiveram uma resposta superior a 5 segundos. Neste caso, apesar a API responder, o DF não tem em conta essa resposta.

Alguns pressupostos a considerar:
* Se o site não for de uma notícia o mais certo é que o resultado seja inconclusivo
* Valida-se sempre qualquer link que seja colocado pelo user, mesmo que não sejam das catergorias mensionadas nas limitações. Espera-se que os users façam bom uso com as indicações que lhe serão prestadas. 

## Ferramentas usadas

A lista de ferramentas usadas, para a construção desta API, são todas open source. Este foi um ponto assente na nossa escolha.

* <b>Github</b> e <b>Github Desktop</b>: para gestão do código
* <b>Jupyter Notebook</b>: para exploração preparação do dataset e construção e validação do modelo. Também foi usado na preparação do scraping.
* <b>Visual Studio IDE</b>: uma ferramenta da Microsoft que ajuda muito na construção do código.
* <b>Heroku</b>: plataforma para deploy do projeto na nuvem
* <b>Dialogflow Essencial</b>: para testar a chamada da API em ambiente chatbot
* <b>Python</b>: linguagem de programação usada

## Roadmap

Esperamos poder vir a fazer no futuro as seguintes melhorias:<br>
* Aumentar as categorias treinadas<br>
* Passar a aceitar mensagens de voz <br>

## Estrutura/setup do projecto

Um projeto desta complexidade e envolvendo tanta tecnologia, foi essencial recorrer à documentação de cada ferramenta. <br>
O código usado em todo o processo é todo em python. 
Os próximos capítulos vão ajudar a compreender melhor o que está feito, não tendo como objetivo entrar em grande profundidade.

### Setup

Para ver os notebooks que auxiliaram na preparação do código final, será necessário instalá-lo. Caso já o tenha, não será necessário fazer nada. Pode recorrer a duas fontes: <br>
* Instalar apenas o jupyter notebook clássico (https://jupyter.org/) 
* Instalar através do Anaconda, que é muito usado pelos Data Science (https://www.anaconda.com/)

Como editor de código, eu usei o [Visual Studio IDE](https://visualstudio.microsoft.com/), que já vem linkado com o Github Desktop. Mas pode usar qualquer outro IDE ou até um simples editor de texto.

Vai ser necessário ter o [Python](https://www.python.org/) instalado no PC. Caso tenha instalado o Anaconda, já tem o python instalado assim como as principais bibliotecas. 

Será necessário criar uma conta no [Github](https://github.com/), para poder clonar o código do projeto para o seu PC.

Terá que criar uma conta no [Heroku](https://www.heroku.com/) para fazer o deploy do código na web. Pode arranjar outras soluções como virtualização na cloud dos grandes players, mas no Heroku pode fazer deploy de até 5 projetos de forma totalmente gratuíta.

A criação de conta no [Dialogflow Essentials](https://dialogflow.cloud.google.com/) não será obrigatório, mas simplifica muito na experimentação da api já na vertente do chatbot. Foi por essa razão que usei, mas pode sempre usar outras ferramentas como por exemplo o Postman ou o SoapUI.

### API do webhook

Para criar um webhook para usar no chatbot, recorri ao Heroku (https://www.heroku.com/). Se não conhece, este site permite fazer deploy de web ou a exposição de API de forma gratuita (com limitação até 5 projetos).

Não é o meu propósito explicar os passos necessários para a criação das APIs, uma vez que há muitos videos na web a ensinar. Caso pretenda experimentar, pode usar a minha API criada para este projeto e que se encontra no código fonte.

### Estrutura do projeto

O projeto está dividido em dois grandes blocos de código, uma para fazer scraping às páginas das notícias e o outro para treinar o modelo na deteção de fakes.

| Ficheiro | Descrição |
| -------- | --------- |
| app.py | Ficheiro principal que recebe as chamadas externas e procede de acordo com o pedido |
| predict.py | Lê os dados, prepara-os e constroi o modelo. Tem também as funções necessárias para analizar o conteúdo da notícia |
| scraping_noticia.py | Serve para interpretar e recolher algum conteúdo de uma página web, tal como o título, a notíca, o autor e a data da notícia | 
| FakeRecogna.xlsx | Ficheiro disponibilizado na web (ver em referências o link) com o dataset classificativo de ~12k notícias | 
| Prepare_data_and_model.ipynb | Ficheiro com o código de preparação do modelo. Não é ficheiro de texto standard e pode ser aberto pelo Jupyter Notebook |
| GetBodyURL.ipynb | Mais um ficheiro de auxilio na parte de scraping |

### Módulos

Estou a considerar um módulo cada ficheiro python com um conjunto de código e funções.<br>
Vou explicar alguns pontos do código, embora os mesmos estejam bem documentados com comentários ao longo do código.

#### Módulo Principal (app.py)

Para o python funcionar com web usei a library "flask".<br>
Apenas tem duas rotas desenvolvidas, a route (/) e a fakenews (/fakenews)

Serve apenas para informar que o serviço está ativo.

> @app.route("/", methods=["GET"])

Este bloco é o detector de fakes (action == 'predict")<br>

> @app.route('/fakenews', methods=['POST'])

A primeira etapa é validar que o URL foi passado. Depois valida o mesmo com uma pequena base de conhecimento de sites confiáveis/fakes e se for encontrado na bd responde de acordo com a informação que tem.<br>
Por último, faz a interpretação do site e leitura dos campos necessários que são passados à função centrar da previsão (predict.valid_url)<br>

#### Módulo Predict (predict.py)

Começa por ler o dataset para um dataframe, prepara e treina o modelo (usado  modelo PassiveAggressive do sklearn).<br>
A função central para validar uma notícia é o "valid_url". Dentro deste tem todas as regras de validação e é de onde saí o resultado para trás.<br>

Regras:<br>
* valida se o autor é confiável.
* se não for, valida o ano da notícia >= 2019
* se for >= 2019 vai validar a notícia
* se não foi conclusívo, vai validar o titulo
     
O processo de validação pode terminar em qualquer ponto, caso a regra seja cumprida. <br>

Pontos a reter:<br>
* os títulos só são considerados se o comprimento > 50 caracteres
* só considera a data se no mesmo existir um número com 4 digitos (correspondente ao Ano)


#### Módulo Scraping (scraping_noticia.py)

Este modulo extrai o conteúdo de um link web (URL). Começa por abrir a página, procura os campos com base numas referências e por fim fecha a página para libertar memória.<br>
Os campos lidos são:
| campo | descrição | regra |
| ----- | --------- | ----- |
| titulo | o título | devolve o valor da tag "title" |
| autor | o autor | procura a palavra "uthor" dentro do valor do atributo "class" de qualquer tag |
| dt | data da notícia (texto) | Muitas vezes a data vem no texto do autor. É usado regular expression para capturar a data, apesar de que apenas é pretendido o ano | 
| body | corpo da notícia | procura os primeiros 3 tag "p" (de parágrafo) com comprimento > 150 caracteres | 


### Executar o projeto:

#### Github e Github Desktop

Começo por criar o projeto em Github e depois ir a "Code" e escolher "Open with GitHub Desktop". No seu caso, deverá clonar o projeto 

<img width="264" alt="github" src="https://user-images.githubusercontent.com/76813386/168889444-c58b0001-fdef-41c9-85c8-c38cdfcdb2e7.PNG">

Isto vai abrir projeto na aplicação no seu PC.

<img width="814" alt="githubdesk" src="https://user-images.githubusercontent.com/76813386/168889538-da76a607-e3c3-4fca-92be-cc7f6a28289e.PNG">

Depois basta carregar o botão "Open in Visual Studio Code" para abrir o Visual Studio com o projeto.

Para sincronizar o código com o branch principal, basta ir ao Github Desktop e fazer "Commit to main". A lista de ficheiros alterados aparece na parte de cima, e as diferenças em relação ao último commit encontram-se no lado direito.

<img width="407" alt="githubdesk_commit" src="https://user-images.githubusercontent.com/76813386/168890631-781abdaf-347a-4c75-8c75-e0e4648ead15.PNG">


#### Testar Código Python

Em qualquer projeto python é sempre recomendado criar um ambiente isolado a que chamamos de environment. Com a evolução das versões do python, assim como das livrarias, se não criar um ambiente para o projeto corre sérios riscos que o mesmo não consiga funcionar daqui a algum tempo. Isto deve-se a faltas de compatibilidade entre versões.

Todo o código que vou apresentar deverá ser executado na linha de comando, no caso do Windows (cmd).

Criar um environment python na pasta à sua escolha (normalmente crio uma pasta de projeto e dentro coloco uma pasta com o código. Na pasta pai é onde crio o environment, uma vez que ele vai criar um conjunto de pastas que não fazem parte do projeto)

> <b>C:\\></b>python -m venv c:\path\to\myenv

Aceder à pasta

> <b>C:\\></b>cd c:\path\to\myenv

Iniciar o environment

> <b>C:\path\to\myenv></b>Scripts\activate.bat

Para executar o código python

> <b>(myenv) C:\path\to\myenv></b>python app.py

Para instalar alguma biblioteca em falta (exemplo pandas) dentro do environment

> <b>(myenv) C:\path\to\myenv></b>pip install pandas


#### Heroku

Para fazer deploy no heroku, deverá ter uma conta já criada (não tem custos).
Eu utilizo os seguintes comandos via command line do windows. (nota: Estou a dar aqui nomes de pastas fictícios, que deverá adaptar para os nomes à sua escolha)

Para trabalhar com o heroku, deverá instalar o "Heroku Cli":

<img width="521" alt="Heroku" src="https://user-images.githubusercontent.com/76813386/168910066-8df13740-62ed-460d-a4f6-78a5d1e00e32.PNG">

Fazer login e criar um apontador para o projeto no heroku

> <b>(myenv) C:\path\to\myenv></b>cd myproject <br>
> <b>(myenv) C:\path\to\myenv\myproject></b>"C:\Program Files\heroku\bin\heroku" login <br>
> <b>(myenv) C:\path\to\myenv\myproject></b>"C:\Program Files\heroku\bin\heroku" git:remote -a pyproject <br>

Fazer o deploy do novo código

> <b>(myenv) C:\path\to\myenv\myproject></b>git add . <br>
> <b>(myenv) C:\path\to\myenv\myproject></b>git commit -am "make it better" <br>
> <b>(myenv) C:\path\to\myenv\myproject></b>git push heroku master <br>

O último comando vai apagar o conteúdo do projeto na web e recriar novamente. <br>
O heroku funciona à base de kubernetes, ou seja, cria uma sala isolada onde vai conter o seu código e vai instalar o python como todas as livrarias que indicar no ficheiro "requirements.txt". Quando o código for executado, a sala deve ter todo o ambiente necessário. 

Para fins de debug pode aceder ao logo do seu projeto. Todos os prints que tenha realizado no código serão enviados para o log.

> <b>(myenv) C:\path\to\myenv\myproject></b>"C:\Program Files\heroku\bin\heroku" logs --tail


Não é necessário indicar o caminho onde o Heroku está instalado, caso prefire pode ter esse caminho na path do windows e nesse caso, não será necessário indicar na linha de comando no exemplos anteriores

#### Dialogflow

Para poder testar a API num ambiente chatbot, usei o Dialogflow Essential.

Ao fazer login, deverá criar um novo agente. Adicionar no fulfillment o URL do seu projeto dado pelo Heroku. Por fim adicionar uma intent que receba uma frase à sua escolha e adicionar um parâmetro obrigatório chamado URL para receber o link.

<img width="465" alt="DF" src="https://user-images.githubusercontent.com/76813386/168911432-c9883213-d81a-4620-a98e-d748c413b387.PNG">

Como teste normalmente vou a "Integrations", escolho "Dialogflow Messenger" e por fim faço "TRY IT NOW".

So simple, like that ;)

## Bibliografia

Documentação do Dialogflow ES: <br>
https://cloud.google.com/dialogflow/es/docs/intents-rich-messages

Criação de environment: <br>
https://docs.python.org/3/tutorial/venv.html

Scrapping with Python: <br>
https://realpython.com/beautiful-soup-web-scraper-python/ <br>

Algoritmo tf-idf-vectorizer: <br>
https://medium.com/@cmukesh8688/tf-idf-vectorizer-scikit-learn-dbc0244a911a <br>

Modelo PassiveAggressiveClassifier: <br>
https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PassiveAggressiveClassifier.html <br>

Como fazer scraping dentro do Heroku: <br>
https://romik-kelesh.medium.com/how-to-deploy-a-python-web-scraper-with-selenium-on-heroku-1459cb3ac76c <br>

Fonte do dataset usado: <br>
https://github.com/Gabriel-Lino-Garcia/FakeRecogna <br>


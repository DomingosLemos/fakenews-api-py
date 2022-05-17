import predict
import scraping_noticia
import flask 
from flask import request
import json
import time
from datetime import datetime, timedelta

app = flask.Flask(__name__)

print('Arranquei----------------')
start=''

@app.route("/", methods=["GET"])
def Hello():
    data = {"msg":"Estou vivo"}
    print("Estou vivo")
    return data 

@app.route('/fakenews', methods=['POST'])
def fakenews():
    print('Entrou na rota "/fakenews"')
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    
    request_data = request.get_json()
    #print ('request_data:', request_data)

    action = request_data['queryResult']['action']
    parameters = request_data['queryResult']['parameters']

    print('action:', action) 

    msg = ""
    resposta = {}

    try:
        request_url = parameters['URL']
    except:
        request_url = ""

    if action == "predict":
        print ('Entrou na action = predict')

        # o campo URL é obrigatório, senão não há notícia para avaliar
        if (request_url==""):
            msg = "Para prever a veracidade de uma notícia tem que nos indicar o link da mesma"
        else:
            res_dominio = predict.valid_dominio(request_url)

            print('URL dominio (1=verdade, 0=fake, -1=não sabe', res_dominio)

            if (res_dominio == 1):
                msg = "A fonte da notícia parece ser credível, mas poderá ..."
            elif (res_dominio == 0):
                msg = "A fonte da notícia vem de um fonte de fakenews já validada por profissonais de jornalísmo"
            else:
                #Necessário entrar dentro da notícia
                title, autor, data, body = scraping_noticia.read_url(request_url)
                msg = predict.valid_url(title, autor, data, body)

                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time (END valid_URL) =", current_time)


        print ('request_url:', request_url)
        print ('msg:',msg)

        resposta = {
            "fulfillmentText": msg,
            "displayText": msg,
            "speech": msg
        }

    elif action == "read_url":
        print ('Entrou na action = read_url')
        title, autor, data, body = scraping_noticia.read_url(request_url)
        msg = []
        msg.append({
            "type": "description",
            "title": title,
            "text": [
                "Autor:",
                autor,
                "Data:",
                data,
                "Notícia:",
                body
            ]
        })

        resposta = {
                "fulfillmentMessages": [
                    {
                        "payload": {
                            "richContent": [
                                msg
                            ]
                        }
                    }
            ]
        }
    return resposta

# run the app
if __name__ == '__main__':
   app.run()
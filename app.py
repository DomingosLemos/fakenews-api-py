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

@app.route('/demo', methods=['GET'])
def demo():
    print('Entrou na "rota /demo"')
    request_action = request.args['action']

    if request_action == "obter_nome_aluno":
        msg = "João"
    elif request_action == "obter_responsavel":
        try:
            request_aluno = request.args['aluno']
            request_aluno_lower = request.args['aluno'].lower()
        except:
            request_aluno = ""

        if request_aluno_lower == 'joão' or request_aluno_lower == 'joao':
            msg =  "O responsável do João Sousa é a mãe Maria Sousa"
        elif request_aluno_lower == 'júlia' or request_aluno_lower == 'julia':
            msg = "O responsável da Júlia Neves é o pai Rui Neves"
        else:
            msg = "Lamento, mas o aluno '"  + request_aluno + "' não existe"
    elif request_action == "consultar_horario_retirada":
        try:
            request_periodo = request.args['periodo']
        except:
            request_periodo = ""

        if request_periodo == 'parcial':
            msg = "A saída do periodo parcial é às 14h00"
        elif request_periodo == 'integral':
            msg = "A saída do periodo integral é às 18h00"
        else:
            msg = "Lamento, mas não percebi qual o periodo pretendido"
    
    print (msg)

    return msg

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

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print('Entrou na rota "/webhook"')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)    

    # extended time by 3 sec to make condition which is execute before webhook deadline occur:
    extended_time = now + timedelta(seconds=3)
    print("extended Time =", extended_time.time())

    # Dialogflow agent json response:
    req = request.get_json(force=True)
    print('-------------')
    print(req)
    print('-------------')


    action = req.get('queryResult').get('action')
    session_id = req.get('session')
 
    reply=''
    conn=''

    if action == 'intent1':
        print("enter into intent1")
        print ('action:', action, 'session_id:', session_id)

        conn = predict.create_DB('fakes_db')
        predict.create_task_table(conn)
        predict.insert_task_table(conn, session_id, None)


         # Added time delay to fail the below 'if condition' of normal response for welcome intent:
        time.sleep(3.5)       

        # if current time is less than or equal to extended time then only below condition becomes "True":
        now = datetime.now()
        if now<=extended_time:
            # make a webhook response for welcome intent:
            reply={ "fulfillmentText": "This is simple intent1 response from webhook",
                    "fulfillmentMessages": [
                            {
                            "text": {
                                    "text": [
                                        "This is simple intent1 response from webhook"
                                    ]
                                }
                            }
                        ],  
                }
        else:
            reply={
                    "followupEventInput": {
                            "name": "extent_webhook_deadline",
                            "languageCode": "en-US",
                            "parameters": {
                                "param":start
                            }
                        }
                }
    

    # Create a chain of followup event. Enter into first follow up event:
    # second intent action:
    if action=='followupevent':
        print("enter into first followup event")

        param = req.get('queryResult').get('outputContexts')[0].get('parameters').get('param')
        print(action,'---------start:', param)

        # Added time delay to fail the below 'if condition' and extend time by "3.5 sec", means right now total time "7 seconds" after webhook execute:
        time.sleep(3.5)
        
        # if current time is less than or equal to extended time then only below condition becomes "True": 
        now = datetime.now()
        if now<=extended_time:
            reply={ "fulfillmentText": "Yea, hi there. this is followup 1 event response for webhook.",
                    "fulfillmentMessages": [
                            {
                            "text": {
                                    "text": [
                                        "Yea, hi there. this is followup 1 event response for webhook."
                                    ]
                                }
                        }
                    ],
                "languageCode": "en",
            }
        else:
            reply={
                    "followupEventInput": {
                            "name": "extent_webhook_deadline_2",
                            "languageCode": "en-US",
                            "parameters": {
                                "param":param
                            }
                        }
                }            
    # Third intent action: 
    if action=='followupevent_2':
        print("enter into second followup event")
        param = req.get('queryResult').get('outputContexts')[0].get('parameters').get('param')

        print(action,'----------start:', param)

        # Added time delay to fail the below condition and extended more time by "3.5 sec", means right now total time "10.5 seconds" after webhook execute:
        time.sleep(3.5)
        
        # below response should be generated for extended webhook deadline:
        reply={ "fulfillmentText": "xxxxxxxxxxx",
                    "fulfillmentMessages": [
                            {
                            "text": {
                                    "text": [
                                        param
                                    ]
                                }
                            }
                        ],
                "languageCode": "en",
            }
        
        print("Final time of execution:=>", now.strftime("%H:%M:%S"))
    return reply


# run the app
if __name__ == '__main__':
   app.run()
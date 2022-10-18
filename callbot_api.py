
from aio_pika import message
from actions.app_constans import *
# API HELPER
import requests
from telegram_admin_api import *
BASE_URL = 'https://rasa-server-meirlen.cloud.okteto.net/webhooks/rest/webhook'
from local_db_for_actions import update_order_id



def cancel_order(order_id):

        if TELEGRAM_IS_PROD == False:
            return '200'

        message = "Cancel&&&&"+str(order_id)

        try:
            data = {
                    'sender': 'admin',
                    'message': message,
                
            }
            print(data)        
            response = requests.post(
                url = BASE_URL,
                json=data
            ).json()
   
        except:
            status_code = None
                   
        return '200'

import multiprocessing


def call_create_order_multi_proccess(tracker,from_address,to_address,price,phone,user_comment,platform):
    p = multiprocessing.Process(target=create_order,args=(tracker,from_address,to_address,price,phone,user_comment,platform))
    p.start()


def create_order(tracker,from_address,to_address,price,phone,user_comment,platform):

        if TELEGRAM_IS_PROD == False:
            print('create_order')
            return 'sjcnjs8cuu'

        # "message":"+77774857133&&&лондон$$париж$$1200т$$текст какой то"
        message = str(phone)+"&&&"+str(from_address)+"$$"+str(to_address)+"$$"+str(price)+"$$"+str(user_comment)

        try:
            data = {
                    'sender': 'admin',
                    'message': message,
                
            }
            print(data)        
            response = requests.post(
                url = BASE_URL,
                json=data
            ).json()
            print(response)
            id =  response['id']
        

        except:
            id = None


        if id != None:
           update_order_id(tracker,id)    



def send_order_info_to_admin_telegram(title,from_address,to_address,phone,platform):
    msg = title+'\n'
    msg +=  phone +'\n\n'
    msg += '🔹 <b>' + str(from_address).strip()+'</b>\n\n'
    msg += '🔹 <b>' + str(to_address).strip()+'</b>\n\n'
    msg += '<b>' + str(platform).strip()+'</b>\n\n'
    send_message_to_telegram_chat(ADMIN_CHAT_ID,msg)



def send_smpp_message(message):
        url = 'http://138.68.87.41:5006/webhooks/rest/webhook'
        try:
            response = requests.post(
                url = url,
                headers={"Content-Type":"application/json"},

                json={
                    'sender': 'admin',
                    'message': message,              
                    }
            )
            
            print(response)
   
        except:
            print('Error')
                   

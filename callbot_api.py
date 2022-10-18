
from actions.app_constans import *
# API HELPER
import requests
from telegram_admin_api import *
import dataclasses
BASE_URL = 'http://138.68.87.41:3001/api/'



def cancel_order(order_id):

        if TELEGRAM_IS_PROD == False:
            return '200'
        print('cancel_order')
        url = BASE_URL +'order'
        try:
            response = requests.put(
                url = url,
                json={
                    'id': order_id,
                    'status': "cancel-by-user",              
                    }
            )
            
            status_code = response.status_code
   
        except:
            status_code = None
                   
        return '200'



def create_order(from_address,to_address,price,phone,user_comment,platform):

        # if TELEGRAM_IS_PROD == False:
        #     print('create_order')
        #     return 'sjcnjs8cuu'

        print('create_order')
        return 'sjcnjs8cuu'
        
        url = BASE_URL +'order'
        try:
            data = {
                    'price': price,
                    'user_comment': user_comment,
                    'from': from_address,
                    'to': to_address,
                    'area': platform,
                    'phone': phone,
                    'status': 'new',                    
                    }
            print(data)        
            response = requests.post(
                url = url,
                json=data
            ).json()
            print(response)
            id =  response['id']
        

        except:
            id = None

        return id


def send_order_info_to_admin_telegram(title,from_address,to_address,phone,platform):
    msg = title+'\n'
    msg +=  str(phone) +'\n\n'
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
                   

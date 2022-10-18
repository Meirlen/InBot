import requests
import subprocess
import json 
import os
from actions.app_constans import *
print(os.getcwd())
from telegram_api import send_message_to_telegram_chat


URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
# if token has expired need to get new token by this cmd : yc iam create-token
IAM_TOKEN = "t1.9euelZqXkZKViYyXypadicaNlZzLiu3rnpWamceRiomUkM6Xl8iVipSTjJfl9PcWO3lp-e9kQgiI3fT3Vml2afnvZEIIiA.DOht3aaX-IVy3BxTozFRISTiZrfuowNfJ_tnKmMqqYKGtzLd5lskoX6iHAsDesPW9KOnbLKMvAdGlQ_Yjtp2Cg"
ID_FOLDER = "b1gp0hehtija7evf2j1g"


def update_token(new_token):
   print('Token updated')
   global IAM_TOKEN
   IAM_TOKEN = new_token

def generate_new_token():
    out = subprocess.Popen(['yc', 'iam', 'create-token'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    new_token = stdout
    print(stdout)
    return new_token

def recognize(data):
    """ Функция распознавания русской речи

    :param IAM_TOKEN: (str)
    :param outh_guest: ответ гостя (bytes)
    :param ID_FOLDER: (str)
    :return text: (str)
    
    """
    # в поле заголовка передаем IAM_TOKEN:
    headers = {'Authorization': f'Bearer {IAM_TOKEN}'}
    
    # остальные параметры:
    params = {
        'lang': 'ru-RU',
        'folderId': ID_FOLDER,
        'sampleRateHertz': 48000,
    }

    response = requests.post(URL, params=params, headers=headers, data=data)
    
    # бинарные ответ доступен через response.content, декодируем его:
    decode_resp = response.content.decode('UTF-8')
    
    # и загрузим в json, чтобы получить текст из аудио:
      
    data = json.loads(decode_resp)
    print(data)
    try:
       text = data['result']
    except:
       error_code = data['error_code']
       if error_code == 'UNAUTHORIZED':
          print('UNAUTHORIZED')
          send_message_to_telegram_chat(ADMIN_CHAT_ID,'⚡ ⛔ Yandex Speech Kit Error!!! \n The token has expired.')
       text = ""
    return text



def transcribe_audio():
   if TELEGRAM_IS_PROD:
      path = "user_audio.ogg"
   else:
      path = "/Users/meirlen/Desktop/bot/y/user_audio.ogg"


   with open(path, "rb") as f:
         data = f.read()
         return recognize(data)

# transcribe_audio()
# generate_new_token()



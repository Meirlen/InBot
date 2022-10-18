
from http.client import responses
from actions.app_constans import *
# API HELPER
import requests
from dataclasses import dataclass
import json
from typing import List
import dataclasses
import multiprocessing
import time


def call_custom_action(conversation_id,action_name,delay = False,delay_time = 10.0):
        if delay:
            time.sleep(delay_time)

        print('call_custom_action')
        action_url = ACTION_ENDPOINT.replace('/webhook','')
        url = action_url +'/conversations/'+str(conversation_id)+'/execute'
        print(url)
        print(action_name)
        try:
            response =  requests.post(
                url = url,
                json={
                    'name': action_name,
                    }
            )
            print(response)
        except:
            print("Error")




def update_slot_by_api(conversation_id,slot_name,value):
        print('call_custom_action')
        action_url = ACTION_ENDPOINT.replace('/webhook','')

        url = action_url +'/conversations/'+str(conversation_id)+'/tracker/events?include_events=AFTER_RESTART'
        print(url)
        try:
            response =  requests.post(
                url = url,
                json={
                    'event': "slot",
                    'name': slot_name,
                    'value': value,
                    'timestamp': 0,

                    }
            )
            print(response)
        except:
            print("Error")




def update_slots_by_api(chat_id,items):
        print('call_custom_action')
        action_url = ACTION_ENDPOINT.replace('/webhook','')

        url = action_url +'/conversations/'+str(chat_id)+'/tracker/events?include_events=AFTER_RESTART'
        print(url)
        response = requests.post(
            url = url,
            headers={"Content-Type":"application/json"},
            data=json.dumps(items)
        ).json()


def get_order_status_by_conversation_id(chat_id):
        print('call_custom_action')
        action_url = ACTION_ENDPOINT.replace('/webhook','')

        url = action_url +'/conversations/'+str(chat_id)+'/tracker'

        try:
            response = requests.get(
                url = url,
            ).json()
            order_status = response['slots']['order_status']

            return order_status

        except:
            return None
   


      

@dataclass
class SlotValue:
    event: str
    name: str 
    value:str
    timestamp:int

def create_item_body_update_slots(slot_name,slot_value):
    return dataclasses.asdict(SlotValue("slot",slot_name,slot_value,0))


def call_custom_action_im_multi_proccess(conversation_id,action_name):
    p = multiprocessing.Process(target=call_custom_action,args=(conversation_id,action_name))
    p.start()

def call_update_slot_by_api_multi_proccess(conversation_id,new_price):
    p = multiprocessing.Process(target=update_slot_by_api,args=(conversation_id,"price_trip",str(new_price)+"₸"))
    p.start()

# у оператора есть 10 сек чтобы ответить, если нет ответа то вызовится по умолчанию
def call_default_action_help_in_10_second(conversation_id,action_name,delay_time = 20.0):
    p = multiprocessing.Process(target=call_custom_action,args=(conversation_id,action_name,True,delay_time))
    p.start()    




# items = []
# items.append(create_item_body_update_slots("from_address",'Point A'))
# update_slots_by_api('77774857133',items)
# call_custom_action_im_multi_proccess()
# print("a")
# call_default_classifier_help_in_10_second("http://localhost:5005",77774857133,"action_admin_bi_direct")
# call_custom_action("http://localhost:5005",77774857133,"action_admin_price_submit",delay=False)
# update_slots_by_api("http://localhost:5005",77774857133)
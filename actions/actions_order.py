from rasa_sdk.types import DomainDict
from rasa_sdk.events import Restarted, SlotSet, EventType,ConversationPaused,ConversationResumed
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, FormValidationAction,  Tracker
from rasa_sdk.events import FollowupAction
from wati import *
from typing import Any, Text, Dict, List, Optional
from math import inf
import datetime
from rasa_sdk.events import ReminderScheduled
from rasa_sdk import Action
from actions.app_constans import *
from helper.Utils import *
from actions.price.zone import *
from actions.price.price_generator import *
from telegram_api import *
from callbot_api import *
from local_db_for_actions import *
from actions.action_helper import *
from orders_db import insert_new_order




# class ActionConfirmOrder(Action):

#     def name(self):
#         return "action_confirm_order"

#     def run(self, dispatcher: CollectingDispatcher, tracker, domain):

#         # send order to the server
#         update_status(tracker,'wait_car')
#         dispatcher.utter_message("Ваш заказ в оброботке...",kwargs=get_phone_number(tracker))
#         order_id = get_created_order_id(tracker) # order_id api return after created on the server

#         if order_id == None:
#             dispatcher.utter_message("Произошла непредвиденная ошибка.Попробуйте чуть позже.",kwargs=get_phone_number(tracker))
#             return None
#         else:
#             update_order_id(tracker,order_id)



#         if is_whatsapp(tracker):
#             title = TITLE_AFTER_CONFIRMED_ORDER+'[header]'+DESC_AFTER_CONFIRMED_ORDER+'\n\n'
#         else:
#             title = TITLE_AFTER_CONFIRMED_ORDER+'\n\n'
#             title += DESC_AFTER_CONFIRMED_ORDER+'\n\n'
        
#         update_status(tracker,'wait_car')
#         show_cancle_btn(tracker,dispatcher,title)

#         return [SlotSet("order_status", "wait_car"),SlotSet("requested_slot", None)]
    



class ActionFlowStepOne(Action):

    def name(self):
        return "action_handle_user_flow_step_1"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        phone_number = tracker.get_slot('phone_number')
        order_status =  get_current_order_status(tracker)
        print('STATUS',order_status)
        merged_address_entitity = get_merged_address_entitity(tracker)



        if order_status == 'wait_car' and merged_address_entitity != None:
                update_status(tracker,'free')
                show_ask_from_address(dispatcher,tracker)
                return [Restarted()]
        else:    
            if order_status == 'free':
                # send order to the server
                update_status(tracker,'wait_car')
                chat_id = tracker.get_slot('chat_id')
                dispatcher.utter_message("Ваш заказ в оброботке...",kwargs=get_phone_number(tracker))

                create_order_by_api(tracker) # order_id api return after created on the server
 



            if is_whatsapp(tracker):
                title = TITLE_AFTER_CONFIRMED_ORDER+'[header]'+DESC_AFTER_CONFIRMED_ORDER+'\n\n'
            else:
                title = TITLE_AFTER_CONFIRMED_ORDER+'\n\n'
                title += DESC_AFTER_CONFIRMED_ORDER+'\n\n'
            

            update_status(tracker,'wait_car')
            show_cancle_btn(tracker,dispatcher,title)

            return [SlotSet("order_status", "wait_car"),SlotSet("requested_slot", None)]
        




  

def show_cancle_btn(tracker,dispatcher,title):

        last_intent = tracker.get_intent_of_latest_message()
        msg = order_header(tracker,title)
        buttons = []

        titles = [CANCEL_BTN_TITLE]
        payloads = ['/cancel_fill_adress']

        for i in range(1):
            buttons.append({"title": "{}".format(
                titles[i]), "payload": payloads[i]})

        dispatcher.utter_button_message(
            msg, buttons=buttons, button_type="reply",kwargs=get_phone_number(tracker))    
 



def create_order_by_api(tracker):
    from_address,to_address,price_trip,phone_number,comment,platform = generate_price_info(tracker)
    call_create_order_multi_proccess(tracker,from_address,to_address,price_trip,phone_number,comment,platform)

    id_user = str(phone_number)[1:]
    insert_new_order(from_address,to_address,price_trip,id_user) # save in templates local db
    send_order_info_to_admin_telegram('Поступил новый заказ!',from_address,to_address,phone_number,platform) 
    send_message_to_telegram_chat(ADMIN_CHAT_ID,'Поступил новый заказ!')           
    





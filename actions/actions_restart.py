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
from requests.models import Response
from actions.app_constans import *
from actions.price.zone import *
from actions.price.price_generator import *
from telegram_api import *
from callbot_api import *
from actions.local_db_for_actions import *
from actions.action_helper import *


class ActionRestart(Action):

    def name(self):
        return "action_restart"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        print("action_restart")
        

        if tracker.latest_message['text'] == None:
            return [Restarted()]

   
        last_msg = tracker.latest_message['text']

        sender = tracker.sender_id
        print('Sender_id'+ str(sender))

       
        if last_msg == 'история backup':  #BACKUP // ADMIN MODE
            send_file_to_telegram_chat(ADMIN_CHAT_ID)

        else:     #// USER_MODE
            phone_number =  get_phone_number_from_slot(tracker)
            order_status =  get_current_order_status(tracker)
            car_arrived_message = get_car_arrived_message(phone_number)

            if car_arrived_message != None:
                title = 'Спасибо за поездку!'
                
            if get_add_text(tracker) != CREATE_NEW_ORDER:
                if order_status == 'wait_car' or order_status == 'car_arrived':
                    if len(get_order_id(phone_number))>0:
                        order_id = get_order_id(phone_number)[0]
                        if cancel_order(order_id) == "200":
                            # Also send to telegram admin chat
                            from_address,to_address,price_trip,phone_number,comment,platform = generate_price_info(tracker)
                            send_order_info_to_admin_telegram('Заказ отменен!',from_address,to_address,phone_number,platform) 
                            send_message_to_telegram_chat(ADMIN_CHAT_ID,'Заказ отменен!')        
                            title = "Заказ отменен."

       
            if get_add_text(tracker) != CREATE_NEW_ORDER:
                title = "Заказ отменен"
                dispatcher.utter_message(title,kwargs=get_phone_number(tracker))
            update_status(tracker,'free')
            show_ask_from_address(dispatcher,tracker)
            return [Restarted()]









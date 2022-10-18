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
from helper.Utils import *
from telegram_api import *
from callbot_api import *
from actions.local_db_for_actions import *
from actions.action_helper import *
from actions.price.address_validator import *
from actions.price.bi_address_validator import *
from actions.price.other_address_validator import *
from telegram_admin_api import *
from rasa_api import call_default_action_help_in_10_second
from AppSingleton import *
INTENT_ADDRESS = 'address'
INTENT_BI_ADDRESS = 'bi_direct'
INTENT_ADDRESS_UNDEFINED = 'address_undefined'




class ValidateAddressForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_address_form"

    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        print('validate_phone_number')
        print(slot_value)

        if IS_DEBUG_MODE:
            name = 'TesttUser'
            user_id = '1289'
            chat_id = None
            platform_id = 'telegram'
        else:    
            name = username_from_meta_data(tracker)
            user_id = user_id_from_meta_data(tracker)
            platform_id = platform_from_meta_data(tracker)


        phone_number = phone_number_validate(slot_value)
   
        dispatcher.utter_message(
                        text="Номер"+str(tracker.latest_message["metadata"]),kwargs=get_phone_number(tracker))


        print('PHONE NUM',phone_number)
        if phone_number == None:
                
                if is_whatsapp(tracker) and slot_value == 'да':
                    if is_auth_user(user_id) == None:
                        insert_new_user(name, user_id, phone_number_from_meta_data(tracker),platform_from_meta_data(tracker))
                    return {"phone_number": phone_number_from_meta_data(tracker),"chat_id":  user_id, "platform_id":  platform_id}
                else:
                    dispatcher.utter_message(
                        text=f"❗ Вы ввели не валидный <b>номер телефона</b>, Попробуйте еще раз",kwargs=get_phone_number(tracker))
                    return {"phone_number":  None}

        else:
            if is_auth_user(user_id) == None:
                    insert_new_user(name, user_id, phone_number,platform_from_meta_data(tracker))

            return {"phone_number":  phone_number,"chat_id":  user_id, "platform_id":  platform_id}



    def validate_from_address(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        print('validate_from_address')
        # print('Human help ability',Settings().get_human_ability())
        update_status(tracker,'free')


        if is_nav_menu_clicked(tracker):
            return {
                "from_address": None
            }
        elif order_id_from_meta_data(tracker) != None: # Template
            return template_mapper(order_id_from_meta_data(tracker),user_id_from_meta_data(tracker))    
        else:    
            
            last_intent = tracker.get_intent_of_latest_message()
            print(last_intent)

            merged_address_entitity = get_merged_address_entitity(tracker)

            slot_value = merged_address_entitity


            if slot_value != None and slot_value != 'TRIGGER':

                house_number,apartment_number,to_house_number = get_house_and_apart_ents(tracker)
                chat_id = chat_id_from_meta_data(tracker)

                res = {}
        
                if last_intent == INTENT_ADDRESS:   #язева 8 ,Чулочно носочная фабрика, цум итд
                    res = from_address_mapper(slot_value,house_number,apartment_number)
                    
                    if res['from_address'] == None: # s?
                        dispatcher.utter_message(slot_value,kwargs=get_phone_number(tracker))

                elif last_intent == INTENT_BI_ADDRESS:   # с язева на муканова
        
                    res,all_trip = from_address_mapper_for_bi_direct(tracker,house_number,apartment_number,to_house_number)
                    price_bot = res.get("price_trip",None)
                    if ADMIN_HELP_FUNCTION:
                        res ['help_human'] = 'price'
                        send_to_admin_price_calculate_help(all_trip,price_bot,chat_id)
                        call_default_action_help_in_10_second(chat_id,"action_admin_price_submit",20.0)


                elif last_intent == INTENT_ADDRESS_UNDEFINED:   # 12 13 кафе жулдыз
                    res = from_address_mapper_for_undefined(tracker)
                    if ADMIN_HELP_FUNCTION:
                        res ['help_human'] = 'intent classifier'
                        send_to_admin_intent_address_classifier_help(res['from_address'],chat_id)
                        call_default_action_help_in_10_second(chat_id,"action_admin_bi_direct")
                else: # 12 13 кафе жулдыз

                    res =  from_address_mapper_other(slot_value,house_number,apartment_number)
    

    
                return res

    def validate_to_address(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        print('validate_to_address')
       
        if is_nav_menu_clicked(tracker):
            return {
                "to_address": None
            }
        else:
            chat_id = chat_id_from_meta_data(tracker)
            res,all_trip = check_to_address(tracker)
            price_bot = res.get("price_trip",None)
            if ADMIN_HELP_FUNCTION:
                res ['help_human'] = 'price'
                send_to_admin_price_calculate_help(all_trip,price_bot,chat_id)
                call_default_action_help_in_10_second(chat_id,"action_admin_price_submit",20.0)


            return res
         


    def validate_from_house_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print('validate_from_house_number')


        last_msg = tracker.latest_message['text']
        if last_msg == '/start' or last_msg == '/history' or last_msg == '/bonus' or last_msg == '/profile':
            return {
                "from_house_number": None
            }
        else:    
            house_numbers = tracker.get_latest_entity_values("house_number")
            from_house_number = tracker.get_slot('from_house_number')

            house_numbers_list = []

            for value in house_numbers:
                house_numbers_list.append(value)

            house_numbers_list = sorted(set(house_numbers_list))

            if len(house_numbers_list) == 2:  # Case for bi_direct_address
                return {"from_house_number": house_numbers_list[1]}

            if len(house_numbers_list) == 1:  # Case for 1 address
                return {"from_house_number": slot_value}



    def validate_from_apartment_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        print('validate_from_apartment_number')

        last_msg = tracker.latest_message['text']
        if last_msg == '/start' or last_msg == '/history' or last_msg == '/bonus' or last_msg == '/profile':
            return {
                "from_apartment_number": None
            }
        else:  

            from_house_number = tracker.get_slot('from_house_number')

            if from_house_number == None:
                return {"from_house_number": slot_value, "from_apartment_number": None}
            else:
                if str(slot_value).lower().strip() == 'далее':
                    slot_value = "STR"
                return {"from_apartment_number": slot_value}



    def validate_order_confirm(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        last_intent = tracker.get_intent_of_latest_message()

        print('validate_order_status last intent: ' + str(last_intent))

        if is_require_human_help(tracker):
            return {"order_confirm": None}
        else:    
            if last_intent == 'confirm':
                print('Клиент создал заказ')

                return {
                        "order_confirm": 'yes', 
                        }
                        
            elif last_intent == 'add_comment':

                return {
                        "requested_slot": 'comments'
                        }
            
            else:


                return {"order_confirm": None}


    def validate_comments(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        last_msg = tracker.latest_message['text']
        if last_msg == '/start' or last_msg == '/history' or last_msg == '/bonus' or last_msg == '/profile':
            return {
                "comments": None
            }
        else:    
            return {"comments": slot_value,"order_confirm": None}




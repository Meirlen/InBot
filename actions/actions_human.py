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
from actions.price.zone import *
from actions.price.price_generator import *
from telegram_api import *
from callbot_api import *
from local_db_for_actions import *
from actions.action_helper import *


class ActionAdminBiDirect(Action):

    def name(self):
        return "action_admin_bi_direct"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain)-> List[EventType]:
        print("action_admin_bi_direct")
     

        if is_require_human_help(tracker):
            # ask_order_confirm(tracker,dispatcher)
            msg,buttons  = get_ask_order_confirm_text(tracker,dispatcher)
            # phone_number = phone_number_from_meta_data(tracker)
            phone_number = tracker.sender_id
            from_address = tracker.get_slot('from_address')
            print("Нужна помощь")
            send_message_with_buttons(phone_number,create_body_order_confirm_ask(msg))

            return [SlotSet("help_human", None)]
        else:
            print("Не нужна помощь")

  
        # return [[SlotSet("help_human", None)],FollowupAction("action_check_address_entity_1")]
        # return [[SlotSet("help_human", None),SlotSet("requested_slot", "order_confirm")],FollowupAction("action_check_address_entity_1")]  
        # # return [[SlotSet("requested_slot", None)],FollowupAction("action_check_address_entity_1")]
        # return [Restarted()]

   

class ActionAdminSingleDirect(Action):

    def name(self):
        return "action_admin_single_address"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain)-> List[EventType]:

        print("action_admin_single_address")

        if is_require_human_help(tracker):
            phone_number = tracker.sender_id
            from_address = from_address_text(tracker)
            send_message(phone_number,create_body_ask_to_address(from_address))
            return [SlotSet("help_human", "reply"),SlotSet("to_address", None),SlotSet("to_house_number", None),SlotSet("requested_slot", "to_address"),FollowupAction("validate_address_form")]

        else:
            print("Не нужна помощь")

   


class ActionAdminPriceSubmit(Action):

    def name(self):
        return "action_admin_price_submit"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain)-> List[EventType]:
        print("action_admin_price_submit")

        if is_require_human_help(tracker):

                        # ask_order_confirm(tracker,dispatcher)
            msg,buttons  = get_ask_order_confirm_text(tracker,dispatcher)
            # phone_number = phone_number_from_meta_data(tracker)
            phone_number = tracker.sender_id
            from_address = tracker.get_slot('from_address')
            print("Нужна помощь")
            send_message_with_buttons(phone_number,create_body_order_confirm_ask(msg))

            return [SlotSet("help_human", None)]
        else:
            print("Не нужна помощь")



class ActionAdminSubmitTemplate(Action):

    def name(self):
        return "action_admin_submit_template"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain)-> List[EventType]:

        print("action_admin_submit_template")

        if is_require_human_help(tracker):
            print("Нужна помощь")

            msg,buttons  = get_ask_order_confirm_text(tracker,dispatcher)
            phone_number = tracker.sender_id
            send_message_with_buttons(phone_number,create_body_order_confirm_ask_after_template(msg))

            print("template uploaded")
            return [SlotSet("help_human", "reply"),SlotSet("requested_slot", "order_confirm"),FollowupAction("validate_address_form")] #,FollowupAction("validate_address_form")

            # return [SlotSet("help_human", None)]
        else:
            print("Не нужна помощь")

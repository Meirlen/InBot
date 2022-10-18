from rasa_sdk.events import Restarted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action
from rasa_sdk.events import FollowupAction
from wati import *
from rasa_sdk.events import ReminderScheduled
from rasa_sdk import Action
from requests.models import Response
from actions.app_constans import *
from actions.price.zone import *
from actions.price.price_generator import *
from telegram_api import *
from callbot_api import *
from local_db_for_actions import *
from actions.action_helper import *


class ActionRestart(Action):

    def name(self):
        return "action_restart"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        print("action_restart")
        
        title = "Заказ отменен."

        order_status =  get_current_order_status(tracker)
        if order_status == 'wait_car' or order_status == 'car_arrived': # cancel active order by
                phone_number = phone_number_from_meta_data(tracker)
            
                if len(get_order_id(phone_number))>0:
                    order_id = get_order_id(phone_number)[0]
                    cancel_order(order_id)
                    # dispatcher.utter_message('Данные очищены 2'+str(order_id),kwargs=get_phone_number(tracker))
                # if cancel_order(order_id) == "200":
                    # dispatcher.utter_message('Данные очищены 3'+str(phone_number),kwargs=get_phone_number(tracker))
                    # Also send to telegram admin chat
                    # from_address,to_address,price_trip,phone_number,comment,platform = generate_price_info(tracker)
                    # send_order_info_to_admin_telegram('Заказ отменен!',from_address,to_address,phone_number,platform) 
                    # send_message_to_telegram_chat(ADMIN_CHAT_ID,'Заказ отменен!')        

                    # dispatcher.utter_message(title,kwargs=get_phone_number(tracker))


        dispatcher.utter_message(title ,kwargs=get_phone_number(tracker))


        show_ask_from_address(dispatcher,tracker)
        return [Restarted()]










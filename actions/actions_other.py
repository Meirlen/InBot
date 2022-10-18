from dis import dis
from numpy import diag
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
import json
import requests
import re
from actions.app_constans import *
from helper.Utils import *
from actions.price.zone import *
from actions.price.price_generator import *
from telegram_api import *
from callbot_api import *
from actions.local_db_for_actions import *
from actions.action_helper import *











class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("I will remind you in 5 seconds.",kwargs=get_phone_number(tracker))

        date = datetime.datetime.now() + datetime.timedelta(seconds=5)
        entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return [reminder]


class ActionDefaultFallback(Action):

    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Извините я вас не поняла",kwargs=get_phone_number(tracker))



class ActionPause(Action):

    def name(self):
        return "action_pause"

    def run(self, dispatcher, tracker, domain)-> List[EventType]:
        print("action_pause")
        return [ConversationPaused()]


class ActionResume(Action):

    def name(self):
        return "action_resume"

    def run(self, dispatcher, tracker, domain)-> List[EventType]:
        print("action_resume")
        return [ConversationResumed()]





class ActionProfile(Action):

    def name(self):
        return "action_profile"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):

        dispatcher.utter_message('Profile',kwargs=get_phone_number(tracker))
        show_profile(dispatcher, tracker)
             

class Action_Service_Menu(Action):

    def name(self):
        return "action_service_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        return [FollowupAction("action_check_address_entity_1")]


class ActionAddComment(Action):

    def name(self):
        return "action_add_comment"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):

        message_title = 'Добавление комментарий к заказу. Максимум 100 символов.'
        buttons = []
        titles = ['Заказать', 'Отменить']
        payloads = ['/confirm', '/cancel_fill_adress']

        for i in range(2):
            buttons.append({"title": "{}".format(
                titles[i]), "payload": payloads[i]})

        dispatcher.utter_button_message(
            message_title, buttons=buttons, button_type="reply",kwargs=get_phone_number(tracker))

        slot_array = [SlotSet("order_status", "comment")]

        return slot_array


class ActionSaveComment(Action):

    def name(self):
        return "action_save_comment"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):

        print('Saved comment!!!!!!!!!!!!!')

        # message_title = 'Добавление комментарий к заказу. Максимум 100 символов.'
        # buttons = []
        # titles = ['Заказать сейчас', 'Отменить']
        # payloads = ['/confirm', '/cancel_fill_adress']

        # for i in range(2):
        #     buttons.append({"title": "{}".format(
        #         titles[i]), "payload": payloads[i]})

        # dispatcher.utter_button_message(
        #     message_title, buttons=buttons, button_type="reply",kwargs=get_phone_number(tracker))

        # slot_array = [SlotSet("order_status", "comment")]

        # return slot_array


def is_auth(user_id):
    return False


  

def show_unauthorized_state(dispatcher, tracker):
    tracker.latest_message  # access metadata

    if IS_DEBUG_MODE:
        name = 'TesttUser'
    else:    
        name = username_from_meta_data(tracker)

    dispatcher.utter_message(
                        text="Номер"+str(tracker.latest_message["metadata"]),kwargs=get_phone_number(tracker))

    msg = '💁 Привет <b>'+str(name)+'!</b> ✋\n\n'
    msg += 'Вас приветствует такси Алем!\n🚕 Чтобы заказать такси в нашем боте вам нужно будет указать номер телефона 📱 или отправьте нажав соответствующую кнопку снизу, в меню.'

    buttons = []

    title = '\U0001F4F1 Отправить мой номер телефона'
    titles = [title]

    payloads = ['']

    for i in range(1):
        buttons.append({"title": "{}".format(
            titles[i]), "payload": payloads[i]})

    dispatcher.utter_message(msg, buttons=buttons, button_type="reply",kwargs=get_phone_number(tracker))



def show_profile(dispatcher, tracker):
    tracker.latest_message  # access metadata

    if IS_DEBUG_MODE:
        name = 'TesttUser'
    else:    
        name = username_from_meta_data(tracker)

    phone_number = get_phone_number_from_slot(tracker)
    chat_id = tracker.get_slot('chat_id')

    msg = str(name)+'\n'
    msg += str(phone_number)+'\n'
    msg += 'chat id: <i>'+str(chat_id)+'</i>\n'

    dispatcher.utter_message(msg,kwargs=get_phone_number(tracker))



class ActionAskPhoneNumber(Action):
    def name(self) -> Text:
        return "action_ask_phone_number"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        if is_whatsapp(tracker):
            show_unauthorized_state_for_whatsapp(dispatcher, tracker)
        else:
            show_unauthorized_state(dispatcher, tracker)
     


class ActionAskFromAddress(Action):
    def name(self) -> Text:
        return "action_ask_from_address"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

         show_ask_from_address(dispatcher,tracker)



class ActionAskToAddress(Action):
    def name(self) -> Text:
        return "action_ask_to_address"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        from_address_text_ = from_address_text(tracker)
        if is_whatsapp(tracker):
            return ask_to_address(tracker,dispatcher)
        else:    
            dispatcher.utter_message('<b>'+from_address_text_+'</b>',kwargs=get_phone_number(tracker))
            return  ask_to_address(tracker,dispatcher)




class ActionAskHouseNumber(Action):
    def name(self) -> Text:
        return "action_ask_from_house_number"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        from_address = tracker.get_slot('from_address')
        msg = '💁  <b>'+str(from_address)+'</b>, Напишите <b>номер дома</b>?'
        dispatcher.utter_message(msg,kwargs=get_phone_number(tracker))


class ActionAskApartmentNumber(Action):
    def name(self) -> Text:
        return "action_ask_from_apartment_number"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:


        from_adress = tracker.get_slot('from_address') 
        from_house_number = tracker.get_slot('from_house_number')

        if is_whatsapp(tracker):
          msg = '[ask_apart]'+str(from_adress)+' '+str(from_house_number)+''
        else:
          msg = '💁  <b>'+str(from_adress)+' '+str(from_house_number)+'</b>, укажите подьезд или квартиру.'
  
        buttons = []

        titles = ['Далее']

        for i in range(1):
            buttons.append({"title": "{}".format(
                titles[i])})

        dispatcher.utter_button_message(
            msg, buttons=buttons, button_type="reply",kwargs=get_phone_number(tracker))    



class ActionFlowStepTwo(Action):

    def name(self):
        return "action_handle_user_flow_step_2"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):

        print('action_handle_user_flow_step_2')

        message_title = 'Ваш заказ принят ,ожидайте автодозвон с номером машины'
        buttons = []
        titles = ['Отменить заказ']
        payloads = ['/cancel_fill_adress']

        for i in range(1):
            buttons.append({"title": "{}".format(
                titles[i]), "payload": payloads[i]})
        dispatcher.utter_button_message(
            message_title, buttons=buttons, button_type="reply",kwargs=get_phone_number(tracker))








class ActionCheckAddressEntity1(Action):

    def name(self):
        return "action_check_address_entity_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain) -> Dict[Text, Any]:
            print("action_check_address_entity_1")

            return trigger_address_form(tracker,dispatcher)




class ActionCheckAddressEntity(Action):

    def name(self):
        return "action_check_address_entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain):

        addresses = tracker.get_latest_entity_values("address_name")

        address_list = []

        for address in addresses:
            address_list.append(address)

        address_list = sorted(set(address_list))

        if len(address_list) == 1:
            return [SlotSet("from_address_for_price", address_list[0])]

        elif len(address_list) == 2:
            return [SlotSet("from_address_for_price", address_list[0]), SlotSet("to_address_for_price", address_list[1])]
        else:
            print("no entities")



class ActionAdmin(Action):

    def name(self):
        return "action_admin"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message("Клиенту успешно отправлено сообщение о прибытий авто в телеграм",kwargs=get_phone_number(tracker))


class ActionAskOrderConfirm(Action):
    def name(self) -> Text:
        return "action_ask_order_confirm"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        print("action_ask_order_confirm")



        if is_require_human_help(tracker):
            dispatcher.utter_message(text=f"💁Минуточку..Мы проверяем введенные данные",kwargs=get_phone_number(tracker))
            return []

        else:

            last_msg = tracker.latest_message['text']

            if last_msg == CONFIRM_TEXT: # when human help handle
                print('when human help handle')

                return [SlotSet("order_confirm", "yes"),FollowupAction("validate_address_form")]

            elif last_msg == '/restart':
                 print('cancel')
                 return [FollowupAction("action_restart")]

            else:        
                msg,buttons  = get_ask_order_confirm_text(tracker,dispatcher)
        
                dispatcher.utter_message(
                    msg, buttons=buttons, button_type="reply",kwargs=get_phone_number(tracker))

                return []


class ActionAskComments(Action):
    def name(self) -> Text:
        return "action_ask_comments"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        message_title = '💁 <b>В комментарий к заказу можете написать примечание которое считаете важным. Примеры:</b> \n\n<i>- нужен универсал </i> \n- <i>предварительный заказ, завтра на 7:00</i>  \n- <i>нас 5 человек, нужен минивэн</i> '
        buttons = []
        titles = [CANCEL_BTN_TITLE]
        payloads = ['/cancel_fill_adress']

        for i in range(1):
            buttons.append({"title": "{}".format(
                titles[i]), "payload": payloads[i]})

        dispatcher.utter_button_message(
            message_title, buttons=buttons, button_type="reply",kwargs=get_phone_number(tracker))

        return []



  







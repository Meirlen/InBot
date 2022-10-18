
from actions.app_constans import *
import requests
from telegram_api import *
import multiprocessing
from AppSingleton import *

def send_to_admin_intent_address_classifier_help(address,chat_id):
    send_message_to_telegram_chat_with_buttons('chat_id='+str(ADMIN_CHAT_ID)+'&text=Помогите расспознать следующий адрес:\n'+address+'&reply_markup={"inline_keyboard": [[{"text": "1 АДРЕСС", "callback_data": "action_admin_single_address,'+str(chat_id)+'"}],[{"text": "2 АДРЕСС", "callback_data": "action_admin_bi_direct,'+str(chat_id)+'"}]]}')

def send_to_admin_price_calculate_help(address,price_bot,chat_id):
    send_message_to_telegram_chat_with_buttons('chat_id='+str(ADMIN_CHAT_ID)+'&text=Помогите посчитать оплату.Маршрут\n'+address+'\nБот посчитал:\n'+str(price_bot)+'\n'+str(chat_id)+'&reply_markup={"inline_keyboard": [[{"text": "ПОДТВЕРДИТЬ", "callback_data": "action_admin_price_submit,'+str(chat_id)+'"}],[{"text": "НЕ ПРАВИЛЬНО", "callback_data": "price_no_correct,'+str(chat_id)+'"}]]}')

def send_to_admin_simple_message(text):
    p = multiprocessing.Process(target=send_message_to_telegram_chat,args=(ADMIN_CHAT_ID,text))
    p.start()

# send_to_admin_2_intent_address_classifier_help('12 12 hcnjnxs', 877777777)

# send_to_admin_price_calculate_help("c язева 78 на муканова","877777777")
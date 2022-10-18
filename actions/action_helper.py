
from actions.app_constans import *
from helper.Utils import *
from local_db_for_actions import *
from actions.price.zone import *
from telegram_api import *
from rasa_sdk import Tracker
from typing import Any, Text, Dict
from rasa_sdk.events import Restarted, SlotSet, EventType,ConversationPaused,ConversationResumed,FollowupAction
from wati import *
from orders_db import *
from actions.price.price_generator import *

def get_current_order_status(tracker):     
        return tracker.get_slot('order_status')    


def get_car_arrived_message(phone_number):                
        users_info = search_user_by_phone_number(phone_number)
        if len(users_info)>0:
                chat_id,status,message,platform =  users_info[0].split('&&')
                if status == 'car_arrived':
                    return message
        return None   

# only whatsapp
def phone_number_from_meta_data(tracker):
    phone_number = tracker.latest_message["metadata"]["phone_number"]
    if phone_number == None:
       return tracker.get_slot('phone_number')
    else:
        return phone_number_validate(phone_number)



def platform_from_meta_data(tracker):
    if IS_DEBUG_MODE:
        platform = 'telegram'
    else: 
        try:   
           platform = tracker.latest_message["metadata"]["platform"]
        except:
           platform = 'admin'    
    return platform



def is_whatsapp(tracker):
    return platform_from_meta_data(tracker) == 'whatsapp'


# use only whatsapp
def get_phone_number(tracker):
    if is_whatsapp(tracker):
       return {'phone_num':  str(phone_number_from_meta_data(tracker)).replace('+','')}
    else:
       return None 


# if templates
def order_id_from_meta_data(tracker):
    try:
        order_id = tracker.latest_message["metadata"]["order_id"]
    except: 
        order_id = None

    return order_id

def user_id_from_meta_data(tracker):
    user_id = tracker.latest_message["metadata"]["user_id"]
    return user_id


def username_from_meta_data(tracker):
    username = tracker.latest_message["metadata"]["user_name"]
    return username

def chat_id_from_meta_data(tracker):
    chat_id = tracker.latest_message["metadata"]["chat_id"]
    return chat_id


def get_add_text(tracker):
    try:
       add_text = tracker.latest_message["metadata"]["add_text"]
    except: 
       add_text = None

    return add_text



def show_ask_from_address(dispatcher,tracker):

    if is_whatsapp(tracker):
        msg = '[start_address_form]'+ BODY_WHATSAPP_ASK_ADDRESS_FROM 

    else:
        msg = '💁  <b>Напишите,откуда поедете?</b>\n\n'
        msg += 'пример:«Алиханова 7 89»\n\n'
        msg += 'или передайте ваше местополажение нажав на кнопку в <b>меню</b>:\n\n ⛳ Отправить геопозицию' 

    buttons = []
    titles = ['\U000026F3 Отправить геопозицию']  # , '\U00002B55 Отменить'
    payloads = ['', ]                             # 'История'

    for i in range(len(titles)):
        buttons.append({"title": "{}".format(
            titles[i]), "payload": payloads[i]})

    dispatcher.utter_message(msg, buttons=buttons, button_type="reply",kwargs=get_phone_number(tracker))
    update_status(tracker,'free')



def generate_price_info(tracker):
    phone_number = tracker.get_slot('phone_number')

    to_address = tracker.get_slot('to_address')
    price_trip =  tracker.get_slot('price_trip')

    from_address = from_address_text(tracker)
    comment = tracker.get_slot('comments')

 

    return str(from_address).strip(),str(to_address).strip(),price_trip,phone_number,comment,platform_from_meta_data(tracker)



def from_address_text(tracker):

    from_address = tracker.get_slot('from_address')


    house_number = str(tracker.get_slot('from_house_number')).replace('[\'','').replace('\']','')
    apartment_number = str(tracker.get_slot('from_apartment_number')).replace('[\'','').replace('\']','')
    if apartment_number == 'STR' or apartment_number == 'ORG':
           apartment_number = '' 
    if house_number == 'STR' or house_number == 'ORG':
           house_number = '' 

 

    address = str(from_address) + " " +str(house_number)+ " " +str(apartment_number)

    return address


def show_location_in_map(tracker,coordinates,district_name):
    if coordinates == None and district_name!=None:
       dist_cords =  get_coordinates_by_district(district_name)
       if dist_cords != None:
          coordinates =  [dist_cords[1],dist_cords[0]]

    if coordinates != None:
        longitude = coordinates[0]
        latitude = coordinates[1]

        chat_id = tracker.get_slot('chat_id')
        platform_id = tracker.get_slot('platform_id')
        print(platform_id)
        if platform_id == 'telegram':
            send_location_to_telegram_chat(chat_id,longitude,latitude)
        else:
            print('Only to telegeam users send location map')    


def is_nav_menu_clicked(tracker):
    last_msg = tracker.latest_message['text']
    if last_msg == '/start' or last_msg == '/history' or last_msg == '/bonus' or last_msg == '/profile':
        return True
    else:
        return False

def is_require_human_help(tracker):
    help_human = tracker.get_slot('help_human')
    if help_human == None or help_human == "reply" :
        return False
    else:
        return True



# def call_human_help(tracker):
#     help_human = tracker.get_slot('help_human')
#     if help_human != None :
#         return True
#     else:
#         return False



def merge_array_values(input_array):
    merge_ent = ''
    if len(input_array) == 0:
         merge_ent = None

    for ent in input_array:
        merge_ent = merge_ent +' '+ ent

    return  merge_ent    



def get_house_and_apart_ents(tracker: Tracker) -> Dict[Text, Any]:
    print('handle_address_entities')

    house_number_ents = []
    apartment_number_ents = []

    ents = tracker.latest_message['entities']

    for pos in range(len(ents)):
        ent_name = tracker.latest_message['entities'][pos]['entity']
        ent = tracker.latest_message['entities'][pos]['value']
 
        if ent_name == 'house_number':
            house_number_ents.append(ent)
        if ent_name == 'apartment_number':
            apartment_number_ents.append(ent)



    house_number_ents_len = len(house_number_ents)
    apartment_number_ents_len = len(apartment_number_ents)

    house_number = None
    to_house_number = None
    if house_number_ents_len > 0:
        house_number = house_number_ents[0] 
    if house_number_ents_len > 1:
        house_number = house_number_ents[0] # from house number
        to_house_number = house_number_ents[1] # to house number

    apartment_number = None
    if apartment_number_ents_len > 0:
        apartment_number = apartment_number_ents[0] 
    if apartment_number_ents_len > 1:
        apartment_number = apartment_number_ents[0] 
        # to_apartment_number = apartment_number_ents[1] 



    return house_number,apartment_number,to_house_number



def get_to_house_ents(tracker: Tracker) -> Dict[Text, Any]:
    print('handle_to_address_entities')

    house_number_ents = []

    ents = tracker.latest_message['entities']

    for pos in range(len(ents)):
        ent_name = tracker.latest_message['entities'][pos]['entity']
        ent = tracker.latest_message['entities'][pos]['value']
 
        if ent_name == 'house_number':
            house_number_ents.append(ent)
       



    house_number_ents_len = len(house_number_ents)

    house_number = None
    if house_number_ents_len > 0:
        house_number = house_number_ents[0] 

    return house_number

def get_merged_address_entitity(tracker: Tracker) -> Dict[Text, Any]:
    print('get_address_entitity')

    addr_ents = []

    ents = tracker.latest_message['entities']

    for pos in range(len(ents)):
        ent_name = tracker.latest_message['entities'][pos]['entity']
        ent = tracker.latest_message['entities'][pos]['value']

        if ent_name == 'address_name':
            addr_ents.append(ent)
  

    return merge_array_values(addr_ents)




def order_header(tracker,title):
         
 
        from_address_text_ = from_address_text(tracker)
        to_address = tracker.get_slot('to_address')
        price_trip = tracker.get_slot('price_trip')
        comment = create_comments_slot(tracker)



        msg = title
        msg += '🔹 <b>' + str(from_address_text_).strip()+'</b>\n\n'
        if to_address != 'STR' and to_address != None:
            msg += '🔸 <b>' + str(to_address.strip())+'</b>\n'


        if is_whatsapp(tracker):
            msg += '[body]'
        else:
            msg += '\n'  


        if is_whatsapp(tracker):
            msg += '[footer]'
        
        if price_trip == None:
            msg +=  '🚕  ' + BOT_NO_COULD_NOT_CALC_COST_MESSAGE
        else:   
            msg +=  '🚕  <b>' + price_trip+'</b>'

        if comment != None and str(comment) != 'not':
            msg += '\n\n<i>«' + comment+'» </i>\n'

        return msg




def show_unauthorized_state_for_whatsapp(dispatcher, tracker):
    tracker.latest_message  # access metadata

    if IS_DEBUG_MODE:
        name = 'TesttUser'
        phone_number = '8777777777'
    else:    
        name = username_from_meta_data(tracker)
        phone_number = phone_number_from_meta_data(tracker)


    dispatcher.utter_message('[login]'+str(name)+'&&'+str(phone_number),kwargs=get_phone_number(tracker))  



def trigger_address_form(tracker,dispatcher):
     

        if IS_DEBUG_MODE:
            user_id = '1289'
            chat_id = None
        else: 
            user_id = user_id_from_meta_data(tracker)
            chat_id = chat_id_from_meta_data(tracker)


 
        
        if is_auth_user(user_id) == None:
            print('un_auth state')
            # if is_whatsapp(tracker):
            #     # skip registration for whatsapp users
            #     show_unauthorized_state_for_whatsapp(dispatcher,tracker)
            #     phone_number = phone_number_from_meta_data(tracker)

            #     dispatcher.utter_message(
            #             text="MetaData: "+str(tracker.latest_message["metadata"]),kwargs=get_phone_number(tracker))
            #     return [SlotSet("phone_number", phone_number),SlotSet("requested_slot", "from_address")]
            # else:   
            #     return [SlotSet("requested_slot", "phone_number")]
                        # skip registration for whatsapp users
            phone_number = phone_number_from_meta_data(tracker)

            return [SlotSet("phone_number", phone_number),SlotSet("requested_slot", "from_address")]
  
        else:

            
            slot_array = []
            requred_slot = tracker.get_slot('requested_slot')


            if requred_slot == 'from_apartment_number':
                latest_msg = tracker.get_latest_entity_values("address_name")
                if is_nav_menu_clicked(tracker):
                    slot_array = [SlotSet("from_apartment_number", None)]
                else:
                    slot_array = [SlotSet("from_apartment_number", latest_msg)]
    
            elif requred_slot == 'from_house_number':
                latest_msg = tracker.get_latest_entity_values("address_name")
                if is_nav_menu_clicked(tracker):
                    slot_array = [SlotSet("from_house_number", None)]
                else:
                    slot_array = [SlotSet("from_house_number", latest_msg)]
            else:
                merged_address_entitity = get_merged_address_entitity(tracker)
                if merged_address_entitity == None:
                    show_ask_from_address(dispatcher,tracker)
                    return [Restarted()]
                else:    
                    slot_array = [
                                SlotSet("to_address",None),
                                SlotSet("from_house_number",None),
                                SlotSet("from_apartment_number",None),
                                SlotSet("comments",None),
                                SlotSet("order_confirm",None),
                                SlotSet("from_address", "TRIGGER")
                                                                        ]



            if IS_DEBUG_MODE:
                user_id = '1289'
                chat_id = None
            else: 
                user_id = user_id_from_meta_data(tracker)
                chat_id = chat_id_from_meta_data(tracker)
                
            print('CHAT_ID '+str(chat_id))
            tracker.latest_message  # access metadata
            phone_number = is_auth_user(user_id)
            if phone_number != None:
                slot_array.append(SlotSet("phone_number", phone_number))
                slot_array.append(SlotSet("chat_id", chat_id))


            return slot_array
       
def send_ask_address_form(phone_number):
         
        templates = get_templates(phone_number)

        text = BODY_WHATSAPP_ASK_ADDRESS_FROM

        if len(templates) == 0:
            send_message(phone_number,text)
        else:
            send_message_with_menu(phone_number,create_body_templates(text,templates))    


def price_mapper(from_address,from_house_number,to_address,to_house_number):

    if from_address != None and to_address!=None:
       price = calculate_price(from_address,from_house_number,to_address,to_house_number)
       return price    
    else:
       return None    
    



def get_ask_order_confirm_text(tracker,dispatcher):
        if is_whatsapp(tracker):
            title = TITLE_AFTER_CREATED_ORDER+'[header]'
        else:
            title = TITLE_AFTER_CREATED_ORDER+'\n\n'+DESC_AFTER_CREATED_ORDER+'\n\n'

        
        msg = order_header(tracker,title)

        buttons = []

       
        titles = [CONFIRM_ORDER_BTN_TITLE,
                    ADD_COMMENT_BTN_TITLE, CANCEL_BTN_TITLE]
        payloads = ['Хорошо', '/add_comment', '/cancel_fill_adress']

        for i in range(len(titles)):
            buttons.append({"title": "{}".format(
                titles[i]), "payload": payloads[i]})

        return msg,buttons        


def dict_to_slot_set(dict):
    slot_array = []
    for x, y in dict.items():
        slot_array.append(SlotSet(x, y))

    return slot_array        



def ask_to_address(tracker,dispatcher):
    print("ask_to_address")


    help_human = tracker.get_slot('help_human')
    if help_human == 'reply':
        print('the man replied')
        last_msg = tracker.latest_message['text']

        res,all_trip =  check_to_address(tracker)
        res["help_human"] = None

        slot_set_array = dict_to_slot_set(res)
        to_address = res.get("to_address", None)
        to_house_number = res.get("to_house_number", None)
        price_trip = res.get("price_trip", None)

        return [SlotSet("help_human", None),SlotSet("to_address", to_address),SlotSet("to_house_number",to_house_number),SlotSet("price_trip",price_trip),FollowupAction("validate_address_form")]


    else:

        if is_whatsapp(tracker):
            from_address_text_ = from_address_text(tracker)
            msg = BOT_ASK_TO_ADDRESS+'[body_to_adress_ask_form]'+from_address_text_
        else:
            msg = BOT_ASK_TO_ADDRESS

        # msg += 'Если у вас несколько адресов укажите их через запятую. <b>Пример:</b>\n\n<i>Алиханова 7, цум</i> '

        buttons = []
        titles = [CANCEL_BTN_TITLE]
        payloads = ['История']

        for i in range(len(titles)):
            buttons.append({"title": "{}".format(
                titles[i]), "payload": payloads[i]})

        dispatcher.utter_message(msg, buttons=buttons, button_type="reply",kwargs=get_phone_number(tracker))

        return []


def check_to_address(tracker):

        res = {}

        from_address = tracker.get_slot('from_address')
        from_house_number = tracker.get_slot('from_house_number')
        merged_address_entitity = get_merged_address_entitity(tracker)
        if merged_address_entitity == None:
            return  {
                        "to_address": None
                    }, None

        else:     

            to_address = merged_address_entitity
            to_house_number = get_to_house_ents(tracker)
            comments = create_comments_slot(tracker)


            res =  {
                        "to_address": to_address,
                        "to_house_number": to_house_number,
                        "comments": comments,
                    }
            res["price_trip"] = price_mapper(from_address,from_house_number,to_address,to_house_number)



            all_trip = str(from_address)+' '+str(from_house_number)+' на '+str(to_address)+' '+str(to_house_number)

            return res,all_trip



def create_comments_slot(tracker):
    comments = ''

    date = tracker.get_slot('date')
    time = tracker.get_slot('time')

    preferences = tracker.get_slot('preferences')

    if date != None:
       comments += date

    if time != None:
       comments += time

    
    if comments == '':
       comments = 'not' 
    else:
       comments = "Предварительный заказ: " + comments

    if preferences != None:
       comments =  comments +'\n Предпочтения: '+ preferences


    return comments

    
# from rasa_api import create_item_body_update_slots
# from rasa_api import update_slots_by_api
# import multiprocessing

# def call_send_order_template_api_multi_proccess(order_id,chat_id):
#     p = multiprocessing.Process(target=send_order_template,args=(order_id,chat_id))
#     p.start()

# def send_order_template(order_id,chat_id):
#     print('Order id:', order_id)
#     res = get_template_by_position(order_id)
#     if len(res) == 1:
#        from_address,to_address,price_trip = res[0].split("$")
#        comments = "not"
       
#        items = []

#        items.append(create_item_body_update_slots("from_address",from_address))
#        items.append(create_item_body_update_slots("from_house_number","STR"))
#        items.append(create_item_body_update_slots("from_apartment_number","STR"))


#        items.append(create_item_body_update_slots("to_address",to_address))
#        items.append(create_item_body_update_slots("to_house_number","STR"))

#        items.append(create_item_body_update_slots("price_trip",price_trip))
#        items.append(create_item_body_update_slots("comments",comments))

#        items.append(create_item_body_update_slots("platform_id","whatsapp"))
#        items.append(create_item_body_update_slots("chat_id",chat_id))
#        items.append(create_item_body_update_slots("phone_number","+"+str(chat_id)))

#        items.append(create_item_body_update_slots("order_status","free"))


#     #    items.append(create_item_body_update_slots("requested_slot","order_confirm"))
#        items.append(create_item_body_update_slots("help_human","template_click"))

       

#        update_slots_by_api("http://localhost:5005",chat_id,items)
#        call_custom_action("http://localhost:5005",chat_id,"action_admin_submit_template")


#        print('User click template: ',price_trip)


def template_mapper(order_id,chat_id):
    print('Order id:', order_id)
    res = get_template_by_position(order_id)
    if len(res) == 1:
       from_address,to_address,price_trip = res[0].split("$")
       comments = "not"
       
       res_slot_map = {}

       res_slot_map["from_address"] = from_address
       res_slot_map["from_house_number"] = "STR"
       res_slot_map["from_apartment_number"] = "STR"

       res_slot_map["to_address"] = to_address
       res_slot_map["to_house_number"] = "STR"
   
       res_slot_map["price_trip"] = price_trip
       res_slot_map["comments"] = "not"


       res_slot_map["platform_id"] = "whatsapp"
       res_slot_map["chat_id"] = chat_id
       res_slot_map["phone_number"] = "+"+str(chat_id)
     
       res_slot_map["order_status"] = "free"
       
       return res_slot_map

    else:
        return None


from rasa_api import create_item_body_update_slots
from rasa_api import update_slots_by_api

def clear_address_form_slots_after_car_arrived(chat_id):
 
       items = []

       items.append(create_item_body_update_slots("from_address",None))
       items.append(create_item_body_update_slots("from_house_number",None))
       items.append(create_item_body_update_slots("from_apartment_number",None))


       items.append(create_item_body_update_slots("to_address",None))
       items.append(create_item_body_update_slots("to_house_number",None))

       items.append(create_item_body_update_slots("price_trip",None))
       items.append(create_item_body_update_slots("comments",None))

       items.append(create_item_body_update_slots("platform_id","whatsapp"))
       items.append(create_item_body_update_slots("order_status","car_arrived"))

       update_slots_by_api(chat_id,items)



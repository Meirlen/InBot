from helper.Utils import *
from actions.local_db_for_actions import *
from rasa_sdk import Action, FormValidationAction,  Tracker
from actions.action_helper import *
from actions.price.address_validator import *
from actions.price.other_address_validator import from_address_mapper_for_undefined

# с язева 7 на муканова 
def from_address_mapper_for_bi_direct(tracker: Tracker,house_number,apartment_number,to_house_number):
    print('from_address_mapper_for_bi_direct')
    res_slot_map = {}

    ents = tracker.latest_message['entities']

    from_addresses = []
    to_addresses = []
    

    for pos in range(len(ents)):
            ent_name = tracker.latest_message['entities'][pos]['entity']
            ent = tracker.latest_message['entities'][pos]['value']
            try:
                entity_role = tracker.latest_message['entities'][pos]['role']
                if entity_role == 'from':
                    from_addresses.append(ent)
                if entity_role == 'to':
                    to_addresses.append(ent)    
            except:
                entity_role = None

            print(ent,': ',ent_name, ' role: ',entity_role)    

    from_address = merge_array_values(from_addresses)
    to_address = merge_array_values(to_addresses)


    print("From address:",from_address)
    if from_address != None:



        if is_require_house_number(from_address) == False:
            if house_number == None:
                    house_number = "STR"

        if is_require_apartment_number(from_address) == False:           
            if apartment_number == None:
                    apartment_number = "STR"


        print('From addr: ', from_address)
        print('To addr: ', to_address)

        

        res_slot_map["from_address"] = from_address    
        res_slot_map["from_house_number"] = house_number
        res_slot_map[ "from_apartment_number"] = apartment_number

        res_slot_map["to_address"] = to_address
        res_slot_map["to_house_number"] = to_house_number
        res_slot_map["comments"] = create_comments_slot(tracker)


        res_slot_map["price_trip"] = price_mapper(from_address,house_number,to_address,to_house_number)

        all_trip = str(from_address)+' '+str(house_number)+' на '+str(to_address)+' '+str(to_house_number)
        return res_slot_map,all_trip

    else:
        res = from_address_mapper_for_undefined(tracker)
        all_trip = res["from_address"]
        return res,all_trip


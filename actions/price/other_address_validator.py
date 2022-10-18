from helper.Utils import *
from actions.local_db_for_actions import *
from rasa_sdk import Action, FormValidationAction,  Tracker
from actions.action_helper import *
from actions.price.address_validator import *

def from_address_mapper_other(address_name,house_number,apartment_number):

    print('from_address_mapper')

    res_slot_map = {}

    if house_number == None:
        house_number = "STR"

    if apartment_number == None:
        apartment_number = "STR"


    res_slot_map["from_address"] = address_name
    res_slot_map["from_house_number"] = house_number
    res_slot_map[ "from_apartment_number"] = apartment_number


    res_slot_map["to_address"] = "STR"

    res_slot_map["comments"] = "not"


    return res_slot_map



def from_address_mapper_for_undefined(tracker: Tracker):

    print('from_address_mapper')

    res_slot_map = {}


    ents = tracker.latest_message['entities']

    all_ents = []

    for pos in range(len(ents)):
        ent_name = tracker.latest_message['entities'][pos]['entity']
        ent = tracker.latest_message['entities'][pos]['value']

        if ent_name == 'address_name' or ent_name == 'house_number'  or ent_name == 'apartment_number':
            all_ents.append(ent)


    res_slot_map["from_address"] = merge_array_values(all_ents)
    res_slot_map["from_house_number"] = "STR"
    res_slot_map[ "from_apartment_number"] = "STR"


    res_slot_map["to_address"] = "STR"
    res_slot_map["comments"] = "not"


    return res_slot_map


    
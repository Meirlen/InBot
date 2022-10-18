
from helper.Utils import *
from actions.local_db_for_actions import *
from dataclasses import dataclass
from enum import Enum


class ADRESS_TYPE(Enum):
    STREET_HOUSE = "0"
    PRIVATE_HOUSE = "1"
    MACRO_AREA = "2"
    OTHER = "4"


@dataclass
class Place:
    name: str
    type: str  # 0 street 1 частный сектор 2 macro_area
    lat: float
    lng: float



def get_address_type(address_name):
    address_name = address_text_pre_proccess(address_name)

    address_type = ADRESS_TYPE.OTHER

    # Step 1: search in local tables
    local_results = (search_by_levenshtein_distance(address_name))


    if len(local_results) > 0:
            source = local_results[0]['source']
            if source == 'location':
                type = local_results[0]['response'].split("^^")[2]
                address_type = type

    return address_type



def is_require_apartment_number(address_name):
    address_type = get_address_type(address_name)
 
    if address_type == ADRESS_TYPE.STREET_HOUSE.value:
        return True
    else:
       return False


def is_require_house_number(address_name):
    address_type = get_address_type(address_name)
 
    if address_type == ADRESS_TYPE.STREET_HOUSE.value or address_type == ADRESS_TYPE.PRIVATE_HOUSE.value:
        return True
    else:
       return False



def from_address_mapper(address_name,house_number,apartment_number):

    print('from_address_mapper')

    res_slot_map = {}

    if is_require_house_number(address_name) == False:
        if house_number == None:
                   house_number = "STR"

    if is_require_apartment_number(address_name) == False:           
        if apartment_number == None:
                   apartment_number = "STR"


    res_slot_map["from_address"] = address_name
    res_slot_map["from_house_number"] = house_number
    res_slot_map["from_apartment_number"] = apartment_number


    return res_slot_map


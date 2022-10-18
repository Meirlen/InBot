from os import replace
import sqlite3
import itertools
from itertools import combinations, count
from random import randrange
from random import randint
import random
from data_generator_str import add_data_to_txt
from data_generator_str import generate_adress_nlu
from data_generator_str import select
from data_generator_str import select_by_type
from data_generator_str import get_street
from data_generator_org import generate_org_key_loc
from data_generator_org import generate_org
from data_generator_str import patterns_street
from data_generator_str import change_entity_key_name
from data_generator_org import change_entity_key_name_for_org
from data_generator_org import generate_org_category_plus_key_random
DB_NAME = 'krg_address.db'



# Patterns
patterns_street_plus_orgs = [
            '?pre ?s ?o',
            '?pre ?s ?2pre ?o',
            '?s ?o',

]

patterns_orgs_plus_street = [      
            '?pre ?o ?2pre ?s',
            '?pre ?o ?s',
            '?o ?s',
            '?o ?2pre ?s',

]

patterns_macro_area = [      
            '?pre ?o ?2pre ?s',
            '?pre ?o ?s',
            '?o ?s',
            '?o ?2pre ?s',

]


pretext_array_street_info_1= ['по','на','в'] 
pretext_array_street_info_2= ['на','в'] 


def generate_street_plus_orgs(pretext,pretext2,street, org, pattern,with_start_pretext = True):

    if with_start_pretext:
        address = pattern.replace('?pre', pretext).replace('?2pre', pretext2).replace('?s', street).replace('?o', org)
    else:
        address = pattern.replace('?pre', '').replace('?2pre', pretext2).replace('?s', street).replace('?o', org)
    return address.strip() 


# Street + orgs
def generate_street_plus_orgs_nlu(count,with_start_pretext = True):

    street_array = generate_adress_nlu(select(),patterns_street,'{"entity": "address_name", "role": "street"}',with_apart_num = False)
    street_array = change_entity_key_name(street_array,'{"entity": "address_name", "role": "street"}')

    org_array = generate_org_key_loc('{"entity": "address_name", "role": "org"}')


    data = []
     
    for x in range(count):
        street = random.choice(street_array).replace("    - ","").strip()
        org = random.choice(org_array).replace("    - ","").strip()

        pretext = random.choice(pretext_array_street_info_1)
        pretext2 = random.choice(pretext_array_street_info_2)

        pattern =  random.choice(patterns_street_plus_orgs)

        item = "    - "+generate_street_plus_orgs(pretext,pretext2,street,org,pattern,with_start_pretext).strip()+'\n'
        data.append(item)


    return data



# Street + orgs
def generate_orgs_plus_street_nlu(count,with_start_pretext = True):

    street_array = generate_adress_nlu(select(),patterns_street,'{"entity": "address_name", "role": "street"}',with_apart_num = False)
    street_array = change_entity_key_name(street_array,'{"entity": "address_name", "role": "street"}')

    org_array = generate_org_key_loc('{"entity": "address_name", "role": "org"}')

    data = []
    for x in range(count):
        street = random.choice(street_array).replace("    - ","").strip()
        org = random.choice(org_array).replace("    - ","").strip()

        pretext = random.choice(pretext_array_street_info_1)
        pretext2 = random.choice(pretext_array_street_info_2)

        pattern =  random.choice(patterns_orgs_plus_street)

        item = "    - "+generate_street_plus_orgs(pretext2,pretext,street,org,pattern,with_start_pretext).strip()+'\n'
        data.append(item)

    return data   





# Street + orgs
def generate_macro_areas_orgs_plus_street_nlu(count,with_start_pretext = True):

    street_array = generate_adress_nlu(select(),patterns_street,'{"entity": "address_name", "role": "street"}',with_apart_num = False)
    street_array = change_entity_key_name(street_array,'{"entity": "address_name", "role": "street"}')

    org_array = generate_org_key_loc('{"entity": "address_name", "role": "org"}')

    macro_areas_array = select_by_type(2)

    data = []
    for x in range(count):
        street = random.choice(street_array).replace("    - ","").strip()
        org = random.choice(org_array).replace("    - ","").strip()
        macro_area = random.choice(macro_areas_array)
        macro_area = f'[{macro_area}]'
        macro_area = macro_area + '{"entity": "address_name", "role": "macro_area"}'

        pretext = random.choice(pretext_array_street_info_2)
        pretext2 = random.choice(pretext_array_street_info_2)

        pattern =  random.choice(patterns_orgs_plus_street)
        
        switcher = randrange(2)
        if(switcher == 0):
            street = org

        item = "    - "+generate_street_plus_orgs(pretext2,pretext,street,macro_area,pattern,with_start_pretext).strip()+'\n'
        data.append(item)

    return data     


def generate_street_info_intent(count,with_start_pretext = True):
    data1 = generate_street_plus_orgs_nlu(count,with_start_pretext)
    data2 = generate_orgs_plus_street_nlu(count,with_start_pretext)
    data3 = generate_macro_areas_orgs_plus_street_nlu(count,with_start_pretext)
    data = data1+data2+data3
    result = sorted(data, key = lambda x: random.random())
    return result


add_data_to_txt(generate_street_info_intent(1300),'/Users/meirlen/Desktop/bot/dataset/street+organization.txt','street+organization')


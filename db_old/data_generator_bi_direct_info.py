from os import replace
import sqlite3
import itertools
from itertools import combinations
from random import randrange

from random import randint
import random
from data_generator_str import add_data_to_txt
from data_generator_str import generate_adress_nlu
from data_generator_str import select
from data_generator_str import get_street
from data_generator_org import generate_org_key_loc
from data_generator_org import generate_org
from data_generator_str import patterns_street
from data_generator_str import change_entity_key_name
from data_generator_org import change_entity_key_name_for_org
from data_generator_street_info import generate_street_info_intent

DB_NAME = 'krg_address.db'



# Patterns
patterns = [
            '[?a]{"address_name"}',
            '[?a]{"address_name"} [?d](house_number)',
            '[?a]{"address_name"} [дом ?d](house_number)',
            '[?a]{"address_name"} [?d дом](house_number)',
            
  ]

pretext_array = ['по','на','в'] # юмит по бабущкина, корзина на юге


pretext_from_array = ['с','со','от','из'] # с майкудука
pretext_to_array = ['до','на','в'] # до язева, до пришахтиска



def generate_bi_direct_info2():

    from_entity = '{"entity": "address_name", "role": "from"}'
    to_entity = '{"entity": "address_name", "role": "to"}'


    patterns_street_from = change_entity_key_name(patterns_street,from_entity)
    patterns_street_to = change_entity_key_name(patterns_street,to_entity)

    # Street
    street_array_from = generate_adress_nlu(select(),patterns_street_from,from_entity)
    street_array_to = generate_adress_nlu(select(),patterns_street_to,to_entity,False)

    # Orgs
    org_array_from = generate_org_key_loc(from_entity)
    org_array_to = generate_org_key_loc(to_entity)

    # Street+info
    street_info_array = generate_street_info_intent(2000,False)


    data = []
     
    for x in range(5000):
        from_key = random.choice(pretext_from_array)
        to_key = random.choice(pretext_to_array)

        switcher = randrange(4)
        if switcher == 0: # street + info
           from_address = random.choice(street_array_from)
           to_address =   random.choice(street_info_array)
        elif switcher == 1: # info + street
           from_address = random.choice(street_info_array)
           to_address =   random.choice(street_array_to)
        elif switcher == 2: # org + info
           from_address = random.choice(org_array_from)
           to_address =   random.choice(street_info_array)
        else: # info + org
           from_address = random.choice(street_info_array)
           to_address   = random.choice(org_array_to) 

        item =from_key+ " "+ from_address.replace('    - ','').strip() + " "+ to_key+" "+ to_address.replace('    - ','').strip()+"\n"
        data.append('    - '+item)      

    add_data_to_txt(data,'/Users/meirlen/Desktop/bot/dataset/bi_direct_info.txt','bi_direct_info')




generate_bi_direct_info2()

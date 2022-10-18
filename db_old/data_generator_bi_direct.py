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



# 3 Intent: street+organization
# Пример : - [улица](key_name) [алданская]{"entity": "address_name", "role": "street"} [81 дом](house_number) [светлана]{"entity": "address_name", "role": "org"}

# Patterns
patterns = [
            '[?a]{"address_name"}',
            '[?a]{"address_name"} [?d](house_number)',
            '[?a]{"address_name"} [дом ?d](house_number)',
            '[?a]{"address_name"} [?d дом](house_number)',
            
  ]

pretext_from_array = ['с','со','от','из'] # с майкудука
pretext_to_array = ['до','на','в'] # до язева, до пришахтиска


  
# 4 Intent: bi_direct
# Пример : со степного 3 дом 67 квартира 89 на цум
#  - от [станиславского]{"entity": "address_name", "role": "from"} [75](house_number) до [к 3 входу](loc_name) [массажный салон](key_name) [new look]{"entity": "address_name", "role": "to"}

def generate_bi_direct(count):
    from_entity = '{"entity": "address_name", "role": "from"}'
    to_entity = '{"entity": "address_name", "role": "to"}'

    patterns_street_from = change_entity_key_name(patterns_street,from_entity)
    patterns_street_to = change_entity_key_name(patterns_street,to_entity)

    # Street
    street_array_from = generate_adress_nlu(select(),patterns_street_from,from_entity)
    street_array_to = generate_adress_nlu(select(),patterns_street_to,to_entity)

    # Orgs
    org_array_from = generate_org_key_loc(from_entity)
    org_array_to = generate_org_key_loc(to_entity)



    data = []
     
    for x in range(count):
        from_key = random.choice(pretext_from_array)
        to_key = random.choice(pretext_to_array)

        switcher = randrange(4)
        if switcher == 0: # street + street
           from_address = random.choice(street_array_from)
           to_address = random.choice(street_array_to)
        elif switcher == 1: # street + org
            from_address = random.choice(street_array_from)
            to_address = random.choice(org_array_to)
        elif switcher == 2: # org + street
            from_address = random.choice(org_array_from)
            to_address = random.choice(street_array_to)    
        else: # org + org
            from_address = random.choice(org_array_from)
            to_address = random.choice(org_array_to)   

        item =from_key+ " "+ from_address.replace('    - ','').strip() + " "+ to_key+" "+ to_address.replace('    - ','').strip()+"\n"
        data.append('    - '+item)       


    add_data_to_txt(data,'/Users/meirlen/Desktop/bot/dataset/bi_direct.txt','bi_direct')

generate_bi_direct(4000)


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




# 1 Нужно заполнить таблицу - lookup: address_name для улучшения расспознавания
# у нас есть 2 основных типов address_name : street & org
# Добавим все sstreet & org из локальной таблицы:
# Пример: натали , авроры итд

def add_data_to_lookup_address_name():
    street_array = get_street(select())
    org_array = generate_org()
    add_data_to_txt(street_array + org_array,'/Users/meirlen/Desktop/bot/dataset/lookup_address.txt')





# 2 Intent: address
# Пример street:  [автомобильная](address_name) [126 дом](house_number), - [улица](key_name) [авроры](address_name) [171 дом](house_number)
# Пример org: 

def add_data_to_intent_address():
    street_array = generate_adress_nlu(select(),patterns_street,'(address_name)')
    org_array = generate_org_key_loc('(address_name)')
    add_data_to_txt(sorted(street_array + org_array, key = lambda x: random.random()),'/Users/meirlen/Desktop/bot/dataset/address.txt')

# add_data_to_intent_address()



# 3 Intent: street+organization
# Пример : - [улица](key_name) [алданская]{"entity": "address_name", "role": "street"} [81 дом](house_number) [светлана]{"entity": "address_name", "role": "org"}

# Patterns
patterns = [
            '[?a]{"address_name"}',
            '[?a]{"address_name"} [?d](house_number)',
            '[?a]{"address_name"} [дом ?d](house_number)',
            '[?a]{"address_name"} [?d дом](house_number)',
            
  ]

pretext_from_array = ['с','со','от','из','на','в'] # с майкудука
pretext_array = ['по','на','в'] # юмит по бабущкина, корзина на юге
pretext_to_array = ['до','на','в'] # до язева, до пришахтиска


pretext_from_array_bi_direct = ['с','со','от','из'] # с майкудука
pretext_to_array_bi_direct = ['до','на','в'] # до язева, до пришахтиска


pretext_array_street_info= ['по','на','в'] 
pretext_array_street_info= ['на','в'] 


def generate_street_plus_org_nlu(
    street_address_name='{"entity": "address_name", "role": "street"}',
    org_address_name = '{"entity": "address_name", "role": "org"}',
    patterns_array = patterns,
    with_pretext = True
):
    data = []
    patterns_array =  change_entity_key_name(patterns_array,street_address_name,'{"address_name"}')
    street_array = generate_adress_nlu(select(),patterns_array,street_address_name)
    org_array = generate_org_key_loc(org_address_name)

    for x in range(8000):
        street = random.choice(street_array).replace("    - ","").strip()
        org = random.choice(org_array).replace("    - ","").strip()
        pretext = random.choice(pretext_array)
        from_key = random.choice(pretext_from_array)

        switcher = randrange(4)
        if with_pretext == True:
            if(switcher == 1):
               data.append("    - "+from_key+' '+street+' '+org+"\n")
            elif(switcher == 2):
               data.append("    - "+from_key+' '+org+' ' +pretext+' '+street+"\n")
            elif(switcher == 3):
               data.append("    - "+from_key+' '+street+' ' +pretext+' '+org+"\n")
            else:
               data.append("    - "+from_key+' '+org+' '+street+"\n")
        else:       
            if(switcher == 1):
               data.append("    - "+street+' '+org+"\n")
            elif(switcher == 2):
               data.append("    - "+org+' ' +pretext+' '+street+"\n")
            elif(switcher == 3):
               data.append("    - "+street+' ' +pretext+' '+org+"\n")
            else:
               data.append("    - "+org+' '+street+"\n")


    

    return data       
  


# 4 Intent: bi_direct
# Пример : со степного 3 дом 67 квартира 89 на цум
#  - от [станиславского]{"entity": "address_name", "role": "from"} [75](house_number) до [к 3 входу](loc_name) [массажный салон](key_name) [new look]{"entity": "address_name", "role": "to"}


def generate_bi_direct():
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
     
    for x in range(8000):
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


    add_data_to_txt(data,'/Users/meirlen/Desktop/bot/dataset/test.txt','bi_direct')






# 5 Intent: bi_direct_info
# Пример : на корзину по абая поедем на бабушкина 
#  {"entity": "address_name", "role": "org"} [корзину]
#  {"entity": "address_name", "role": "street"} [абая]
#  {"entity": "address_name", "role": "to"} [бабушкина]


# Пример : с бабушкина поедем  на корзину по абая 
#  {"entity": "address_name", "role": "from"} [бабушкина]
#  {"entity": "address_name", "role": "to_org"} [корзину]
#  {"entity": "address_name", "role": "to_street"} [абая]

def generate_bi_direct_info():
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


    # Orgs + info
    org_plus_info_from_array =  generate_street_plus_org_nlu(
        '{"entity": "address_name", "role": "street"}',
        '{"entity": "address_name", "role": "org"}',
        with_pretext = False
        )

    org_plus_info_to_array =  generate_street_plus_org_nlu(
        '{"entity": "address_name", "role": "to_street"}',
        '{"entity": "address_name", "role": "to_org"}',
         with_pretext = False

        )


    data = []
     
    for x in range(8000):
        from_key = random.choice(pretext_from_array)
        to_key = random.choice(pretext_to_array)
        
        switcher = randrange(4)
        if switcher == 0: # street + info
           from_address = random.choice(street_array_from)
           to_address = random.choice(org_plus_info_to_array)
        elif switcher == 1: # info + street
           from_address = random.choice(org_plus_info_from_array)
           to_address =random.choice(street_array_to)
        elif switcher == 2: # org + info
           from_address = random.choice(org_array_from)
           to_address = random.choice(org_plus_info_to_array)
        else: # info + org
           from_address = random.choice(org_plus_info_from_array)
           to_address = random.choice(org_array_to)   


        item =from_key+ " "+ from_address.replace('    - ','').strip() + " "+ to_key+" "+ to_address.replace('    - ','').strip()+"\n"
        data.append('    - '+item)       

    add_data_to_txt(data,'/Users/meirlen/Desktop/bot/dataset/bi_direct_info.txt','bi_direct_info')


 # Пример : с бабушкина поедем  на корзину по абая 
#  {"entity": "address_name", "role": "from"} [бабушкина]
#  {"entity": "address_name", "role": "to_org"} [корзину]
#  {"entity": "address_name", "role": "to_street"} [абая]

def generate_bi_direct_2info():
  
    # Orgs + info
    org_plus_info_from_array =  generate_street_plus_org_nlu(
        '{"entity": "address_name", "role": "street"}',
        '{"entity": "address_name", "role": "org"}',
         with_pretext = False

        )

    org_plus_info_to_array =  generate_street_plus_org_nlu(
        '{"entity": "address_name", "role": "to_street"}',
        '{"entity": "address_name", "role": "to_org"}',
        with_pretext = False

        )


    data = []
     
    for x in range(8000):
        from_key = random.choice(pretext_from_array)
        to_key = random.choice(pretext_to_array)
        from_address = random.choice(org_plus_info_from_array)
        to_address = random.choice(org_plus_info_to_array)
    

        item =from_key+ " "+ from_address.replace('    - ','').strip() + " "+ to_key+" "+ to_address.replace('    - ','').strip()+"\n"
        data.append('    - '+item)       

    add_data_to_txt(data,'/Users/meirlen/Desktop/bot/dataset/bi_direct_2info.txt','bi_direct_2info')


# add_data_to_lookup_address_name()
# add_data_to_intent_address()
generate_street_info_intent()
add_data_to_txt(generate_street_plus_org_nlu(),'/Users/meirlen/Desktop/bot/dataset/street+org.txt','street+organization')
# generate_bi_direct()
generate_bi_direct_info()
generate_bi_direct_2info()


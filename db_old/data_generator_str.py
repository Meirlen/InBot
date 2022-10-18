import sqlite3
import itertools
from itertools import combinations
from random import randrange

from random import randint
import random


DB_NAME = 'krg_address.db'

# Patterns
patterns_street = [
            '[?a](address_name)',
            '[?a](address_name)',
            '[?a](address_name)',
            '[?a](address_name)',
            '[?a](address_name) [?d](house_number)',
            '[?a](address_name) [дом ?d](house_number)',
             '[?a](address_name) [?d дом](house_number)',
            '[?a](address_name) [дом ?d](house_number) [квартира ?p](apartment_number)',
             '[?a](address_name) [?d](house_number) [квартира ?p](apartment_number)',
            '[?a](address_name) [дом ?d](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p квартира](apartment_number)',
             '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d дом](house_number) [?p](apartment_number)',
             '[?a](address_name) [?d дом](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [дом ?d](house_number) [квартира ?p](apartment_number)',
            
  ]



# Keys
keys = [
        'проспект',
        'улица',
        'переулок',
]




# TYPE: 
# 0 - улица многоэтажка 
# 1 - улица частный сектор 
# 2 - район(майкудук, пришахтиск)


# SELECT Operation
def select():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION")
    
    result = []

    for row in cursor:
        result.append(str(row[1])+"^^"+str(row[4]))

    conn.close()
    return result

# SELECT Operation
def select_by_type(type):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION WHERE TYPE = '%s'" % type)
    
    result = []

    for row in cursor:
        result.append(str(row[1]))

    conn.close()
    return result
def add_data_to_txt(contents,file_path,intent_name = None):
    file = open(file_path,"w")
    if intent_name != None:
       file.write('- intent: '+intent_name+''+"\n")
       file.write('  examples: |'+"\n")
    file.writelines(contents)
    file.close()


def generate_adress(address, pattern,with_apart_num = True):

      house_number = str(randint(0, 200))
      apart_number = str(randint(0, 500))
      key = "[" + random.choice(keys)+"](key_name)"
      if(with_apart_num):
        address = pattern.replace('?a', address).replace('?d', house_number).replace('?p', apart_number)
      else:  
        address = pattern.replace('?a', address).replace('?d', house_number).replace('[?p](apartment_number)', '').replace('[?p квартира](apartment_number)', '').replace('[квартира ?p](apartment_number)', '')

      switcher = randrange(4)
      if(switcher == 0):
         address = key + ' '+ address
    

      return address.strip()


def generate_adress_nlu(adress_array,patterns,address_entity_name,with_apart_num = True):
    data = []
     
    for obj in adress_array:
        street,type =  obj.split("^^")
        if type == '2': # Если район то не применяем паттерн
           street = street.replace("    - ","").strip()
           data.append("    - ["+street+"]"+address_entity_name+"\n")            
        else:
           pattern = random.choice(patterns)
           street = street.replace("    - ","").strip()
           data.append("    - "+generate_adress(street,pattern,with_apart_num)+"\n")

    return data

# Generate data for -loockup address 
def get_street(street_data):
    data = []
 
    for obj in street_data:
        street,type =  obj.split("^^")
        # street = "[" + street+"](address_name)"
        res = street    
        data.append("    - "+res.lower().strip()+"\n")

    print('Total data: ', len(data))
    return  data



# # 1 add street to - lookup: address_name
# add_data_to_txt(get_street(select()),'/Users/meirlen/Desktop/bot/dataset/street.txt')

# # 2 add street to intent: address
# add_data_to_txt(generate_adress_nlu(select(),patterns,'(address_name)'),'/Users/meirlen/Desktop/bot/dataset/street_nlu.txt')


def change_entity_key_name(patterns_street,new_key,key = '(address_name)'):
    result = []
    for pattern in patterns_street:
        result.append(pattern.replace(key,new_key))
    return result    


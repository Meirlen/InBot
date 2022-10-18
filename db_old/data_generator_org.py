import sqlite3
from pre_proccess import clear
from itertools import combinations
from random import randrange
from random import randint
import random

DB_NAME = 'krg_address.db'
ORG_NAME = 'NAME_ORIGIN'


# Keywords
malls_keyword = [
"торговый центр","магазин одежды", "развлекательный центр","торговый дом",
"трц" ,"магазин мебели","универмаг","cтроительный гипермаркет"
,"магазин обоев", "магазин сантехники", "стройматериалы оптом", "супермаркет", 
"товары для дома", "магазин хозтоваров и бытовой химии"]


shops_keyword = ["магазин","магазин пива", "магазин рыбы и морепродуктов","магазин мяса и колбас",
 "магазин продуктов" ,"мини маркет","магазин алкогольных напитков"
,"интернет-магазин", "продуктовый магазин"]

beauties_keyword = ["cалон красоты","массажный салон","cпа-салон","парикмахерская","ногтевая студия",
            "Косметология","Медцентр","клиника косметология","Фитнес-клуб"]

gas_stations_keyword = ["заправка","азс"]

hospitals_keyword = ["Медцентр","больница","клиника","поликлиника","Диспансер",
            "родильный дом","роддом","детская больница","детская больница","Больница для взрослых","псих больница"]

hotels_keyword = ["Гостиница","гостиничный комплекс","хостел","Санаторий","отель","хостел","Дом отдыха"]

pharmacies_keyword = ["аптека"]

sport_keyword = ["Фитнес клуб","спортивный зал", "тренажёрный зал","Спортивный комплекс","Бассейн","Центр йоги","оздоровительный центр"
]

food_keyword = ["Ресторан","кафе", "караоке клуб","клуб","Бар","пиццерия","быстрое питание"
, "кофейня","клуб","Бар","пиццерия","быстрое питание"]





CATEGORIES = {
    'MALL':malls_keyword,
    'SUPERMARKET':malls_keyword,
    'SHOP':shops_keyword,
    'BEAUTY':beauties_keyword,
    'AZS':gas_stations_keyword,
    'HOTEL':hotels_keyword,
    'SPORT':sport_keyword,
    'FOOD':food_keyword,
    'UNIVER':None,
    'SCHOOL':None,
    'HOSPITAL':None,
    'PARK':None,
    'STADIUM':None,
    'BUS_STATION':None,
    'BAZAR':None,
    'BUS_STOP':None,

}

keyword_array = [malls_keyword,malls_keyword,shops_keyword,
beauties_keyword,gas_stations_keyword,hotels_keyword,sport_keyword,food_keyword]

# Loc desc
loc_desc = ["главный вход","служебный вход","с правой стороны",
              "с левой стороны","спереди","сзади","с торца","возле"
              "возле парковки","около парковки","около стоянки", "около",  "с торца", "снизу", 
            "к 1 входу","к 2 входу",
            "к 3 входу"]



# TYPE: 0 - street, 1 - organiztion
# SELECT Operation
def select(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from ORGANIZATION WHERE CATEGORY = '%s'" % name)
    
    result = []

    for row in cursor:
        result.append(str(row[1]))

    conn.close()
    return result



def add_data_to_txt(contents,file_path):
    file = open(file_path,"w")
    file.writelines(contents)
    file.close()


# Organization + key_name + loc_name 
# 100% = Organization + key_name
# 100% = Organization + key_name + loc_name 
# Example:  - [массажный салон](key_name) [весна](address_name) [к 3 входу](loc_name)
# 
def generate_org_category_plus_key_random(category_data,keyword_data,loc_desc,address_entity_name):
    data = []

 
    for obj in category_data:
        obj = "[" + obj.strip()+"]"+address_entity_name
        if keyword_data !=None:
           key = random.choice(keyword_data)
           key = "[" + key+"](key_name)"
           res = key+ " " + obj
           switcher = randrange(3)
           if(switcher == 0):
               res = obj
           else:
               res = key+ " " + obj    
        else:
           res = obj    

        data.append("    - "+res.lower().strip()+"\n")


    org_keyword_data = data
    size = len(data)
    twenty_percent = (size/100)*25
    # 25 percent loc_desc data 
    result = sorted(org_keyword_data, key = lambda x: random.random())
    org_keyword_loc_data = []
     
    for x in range(int(twenty_percent)):

        org_keyword_data_item = random.choice(result).replace("    - ","").strip()
        desc = random.choice(loc_desc)
        desc = "[" + desc+"](loc_name)"

        switcher = randrange(3)
        if(switcher == 0):
            org_keyword_loc_data.append("    - "+org_keyword_data_item + " "+ desc+"\n")
        else:
            org_keyword_loc_data.append("    - "+desc + " "+ org_keyword_data_item+"\n")

    merged_data = result+org_keyword_loc_data



    return  sorted(merged_data, key = lambda x: random.random())


# Generate data for -loockup address 
def get_orgs(category_data):
    data = []
 
    for obj in category_data:
        # obj = "[" + obj+"](address_name)"
        res = obj    
        data.append("    - "+res.lower().strip()+"\n")

    return  data



def generate_org_key_loc(address_entity_name):
    data =[]
    for category in CATEGORIES:
        db_data = select(category)
        org_data = generate_org_category_plus_key_random(db_data,CATEGORIES[category],loc_desc,address_entity_name)
        data = data+org_data

        # print(category , '   ', len(db_data), ' generated data size: ', len(org_data))

    # print('Total data: ', len(data))
    return data





def generate_org():
    data =[]
    for category in CATEGORIES:
        db_data = select(category)
        org_data = get_orgs(db_data)
        data = data+org_data

        # print(category , '   ', len(db_data), ' generated data size: ', len(org_data))

    # print('Total data: ', len(data))
    return data


# # 1 add organization to - lookup: address_name
# add_data_to_txt(generate_org(),'/Users/meirlen/Desktop/bot/dataset/org.txt') 
# # 2 add org_loc_key to intent: address
# add_data_to_txt(generate_org_key_loc(),'/Users/meirlen/Desktop/bot/dataset/org_loc_key.txt') 





# print(generate_street_org())

def change_entity_key_name_for_org(patterns_org,new_key):
    result = []
    for pattern in patterns_org:
        result.append(pattern.replace('{"address_name"}',new_key))
    return result    

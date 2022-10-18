import re
import requests
import json
from requests.models import Response
from pre_proccess import clear
from local_db_orgs import insert

# Docs: https://yandex.com/dev/maps/geosearch/doc/examples/geosearch_examples.html

# Define the API Key.
API_KEY = 'c7758c48-a2d6-4d6b-8380-45a648be1947'



# Search
def search_place(name):
    text = name+", караганда"

    r = requests.get('https://search-maps.yandex.ru/v1/',
    params = {
        "text": text,
        "ll": "73.107486,49.790359",
        "lang": "ru_RU",
        "apikey": API_KEY,
        "spn": "3.552069,2.400552",

        })


    response = r.json()
    response_array = response['features']

    try:
       response_array = response['features']
       return response_array
    except:   
       return None

    # result = []

    # for item in response_array:
    #     print("---------")
    #     property = item["properties"]
    #     meta_data = property["CompanyMetaData"]
    #     categories = meta_data["Categories"]
    #     coordinates = item["geometry"]["coordinates"]
    #     print(coordinates)
    #     print(property["name"]+ ", "+meta_data["address"])
    #     print("---------")
    #     print("---------")


def contain(list,word):
     is_contain = False
     for item in list:  
         if word == item:
             is_contain = True
             
     return is_contain         
 



# Search
def get_placec_by_category(name):
    text = name+", караганда"

    r = requests.get('https://search-maps.yandex.ru/v1/',
    params = {
        "text": text,
        "ll": "73.107486,49.790359",
        "lang": "ru_RU",
        "apikey": API_KEY,
        "spn": "3.552069,2.400552",
        "type": "biz",
        "results": "1000",

        })


    print(r.url)

    response = r.json()
    response_array = response['features']

    result = []

    for item in response_array:
        property = item["properties"]
        meta_data = property["CompanyMetaData"]
        categories = meta_data["Categories"]
        coordinates = item["geometry"]["coordinates"]
        address = meta_data["address"].replace("Казахстан, Караганда, ","")
        print(property["name"],"   ",address)

        result.append(property["name"].lower().replace("аптека","").replace("магазин","").replace("минимаркет","").strip())

    # no_double_result = set(result)
    # for item in no_double_result:
    #     print("    -",item)




# Search and add to local db
def get_placec_by_category(name,category,keywords):
    text = name+", караганда"

    r = requests.get('https://search-maps.yandex.ru/v1/',
    params = {
        "text": text,
        "ll": "73.192037,49.869069",
        "lang": "ru_RU",
        "apikey": API_KEY,
        "spn": "3.552069,2.400552",
        "type": "biz",
        "results": "20000",
        "skip": "500",

        })


    print(r.url)

    response = r.json()
    response_array = response['features']

    result = []

    for item in response_array:
        property = item["properties"]
        meta_data = property["CompanyMetaData"]
        categories = meta_data["Categories"]
        coordinates = item["geometry"]["coordinates"]

        name = clear(property["name"])

        
        if not name:
            print('empty')
        else: 
            if contain(result,name):
                print ('-')
            else:
            #   print(name)
              result.append(name) 
              address = meta_data["address"].replace("Казахстан, Караганда, ","")
              for key in keywords:
                  name = name.replace(key.lower(),"")
              
            #   if name:
            #      area = get_district(coordinates[1],coordinates[0])
            #     #  insert(name,area,category,address,"","",coordinates[1],coordinates[0])
            #      print(clear(name))
                






    print(len(set(result)))
    print(len(result))

keywords = ["Автосервис","Автомойка","автотехцентр", "автоцентр","Автосалон","Магазин автозапчастей","Автостёкла","Шиномонтаж"
, "Магазин автозапчастей и автотоваров"
]
# get_placec_by_category("Остановка общественного транспорта","BUS_STOP2",keywords)
# get_placec_by_category("Супермаркет","SUPERMARKET")
# get_placec_by_category("Магазин продуктов","SHOP")



#трц
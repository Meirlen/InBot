from http.client import responses
import requests

API_KEY = 'c4ad8581-d6a6-447f-8ca0-fe9c5d55cb51'  # yandex

def geo_coder_yandex(lng,lat):

        geocode = lng+','+lat

        r = requests.get('https://geocode-maps.yandex.ru/1.x/',
                        params={
                            "geocode": geocode,
                            "apikey": API_KEY,
                            "format": "json",
                        })

        response = r.json()
        response_array = response['response']['GeoObjectCollection']['featureMember']
        res = None
        if len(response_array) > 0:
            text = response_array[0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
            text = text.replace('Казахстан, Караганда, ','')
            res = text.lower()

        res = res.replace(',','').replace('-й','').strip() 
        return res   



# YANDEX API
# Docs: https://yandex.com/dev/maps/geosearch/doc/examples/geosearch_examples.html

# Define the API Key.
API_KEY_SEARCH = 'c7758c48-a2d6-4d6b-8380-45a648be1947'

# Search
def search_place(name):
    text = name+", караганда"

    r = requests.get('https://search-maps.yandex.ru/v1/',
    params = {
        "text": text,
        "ll": "73.107486,49.790359",
        "lang": "ru_RU",
        "apikey": API_KEY_SEARCH,
        "spn": "3.552069,2.400552",

        })


    response = r.json()

    try:
       response_array = response['features']
       return response_array
    except:   
       return None        






def get_coordinates_by_yandex_api(address_name):
        print('start search in yandex api:  ' + address_name)
        response_array = search_place(address_name)
        if response_array != None:

            coordinates = None
            size_response = len(response_array)

            if response_array == None or size_response == 0: # if yandex limit return None
                print("no result")
                return coordinates

            else :
                try:
                    print('Yandex found 1 address')

                    item = response_array[0]
                    property = item["properties"]
                    name =  property["name"]
                    coordinates = item["geometry"]["coordinates"]
                    return coordinates

                except:
                    return coordinates
        else:
            return None


# print(get_coordinates_by_address_name('поликлиника на прудах'))

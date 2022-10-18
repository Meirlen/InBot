import googlemaps
import time
import re
from transliterate import translit

# Docs: https://googlemaps.github.io/google-maps-services-python/docs/index.html

# Define the API Key.
API_KEY = 'AIzaSyAVM-EHX_eliKWAL-uUoHxV3RQzEc_Nuec'


# Validation process

def is_contain_name(sentence,txt):
    print(sentence)
    sentence = sentence.lower()
    sentence = re.sub(r'[^\w]', ' ', sentence)
    sentence_ru = translit(sentence, 'ru')
    print(sentence_ru)
    print("-------------------")
    print("-------------------")

    if txt in sentence:
        return True
    else:
        return False




# Search
def search_place(name):
     # Define the Client
     gmaps = googlemaps.Client(key = API_KEY)

     # pre proccess
     name = name.lower()

     # парк в майкудуке шыгыс цум корзина
     query_result  = gmaps.places(query= name+', караганды', location = 'Karagandy, Kazhakhstan',language ="ru")

     #print(query_result)
     print(len(query_result['results']))

     size = len(query_result['results'])
   #   if size > 1:
   #      print('Найдено больше 1 ')  
   #   else:
   #      print('Найдено  1 ')  



    

     for result in query_result['results']:
        #  print(result['types'])
        #  print(result['formatted_address'] + '   name:'+ result['name'] + '   geometry:'+ str(result['geometry']['location']['lat']))
        #  is_contain_name(result['name'],name)
           address = re.sub(r'[^\w]', ' ', result['name'].strip().lower())
           print("    - "+ address) 

   #   for result in query_result['results']:
   #       is_contain_name(result['name'],name)
   #    #           print("True "+ result['formatted_address'] + '   name:'+ result['name'] + '   geometry:'+ str(result['geometry']['location']['lat']))
   #    #   else:
   #    #           print("False "+ result['formatted_address'] + '   name:'+ result['name'] + '   geometry:'+ str(result['geometry']['location']['lat']))
     

search_place("аптеки")




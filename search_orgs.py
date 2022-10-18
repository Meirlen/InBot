
from operator import le
import re
import sqlite3
from matplotlib.pyplot import stem
from nltk.stem import SnowballStemmer
import textdistance
from  helper.Utils  import read_data_from_txt
from helper.Utils import add_data_to_txt 

DB_NAME = 'krg_address.db'

def stemmer(text):
    stemmer = SnowballStemmer("russian")
    return stemmer.stem(text)

def myFunc(e):
    return e['dist']


def select():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION")

    result = []

    for row in cursor:
        result.append(str(row[2])+"^^"+str(row[5])+"^^"+str(row[4])+"^^"+str(row[0])+"^^"+str(row[1]))

    conn.close()
    return result


def select_orgs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from ORGANIZATION")

    result = []

    for row in cursor:
        result.append(str(row[3])+"^^"+str(row[6])+"^^"+str(row[7]) +
                      "^^"+str(row[5])+"^^"+str(row[8])+"^^"+str(row[9])+"^^"+str(row[0])+"^^"+str(row[1]))


    conn.close()
    return result



def search_by_levenshtein_distance(name):

    res_from_locations_db = select()
    res_from_organiztions_db = select_orgs()
    total_res = res_from_locations_db+res_from_organiztions_db

    name = re.sub(r'[^\w]', ' ', name.strip().lower())
    name_origin = name
    name = stemmer(name).strip()

    print("search_by_levenshtein_distance: ", name)

    result = []

    for item in total_res:
        array_res = item.split("^^")
        stem_name = array_res[0].strip()
        source_data = 'location'
        if len(array_res) == 8: # from_orgs
             source_data = 'org'
        else: # from_loc
            source_data = 'location'

        dist = textdistance.levenshtein.distance(name, stem_name)

        if name == stem_name:
        # if dist <= 1:
            result.append({'response': item, 'dist': dist , 'source': source_data })
            if dist == 0:
                result.sort(key=myFunc)
                return result

    result.sort(key=myFunc)
    return result



# address_name = 'феллиды'

# local_results = (search_by_levenshtein_distance(
#             address_name))
# print(local_results)           
# print(local_results)


# res = read_data_from_txt('/Users/meirlen/Desktop/bot/dataset/test/alem_data/street.txt')
# not_found_addrs = []
# found_1_addrs = []
# found_2_addrs = []

# for item in res:
#     address_name = item
#     local_results = (search_by_levenshtein_distance(
#             address_name, total_res))
#     if len(local_results) == 0:
#        not_found_addrs.append(address_name)
#     if len(local_results) == 1:
#        found_1_addrs.append(address_name+'  $$  '+str(local_results[0]))
#     if len(local_results) == 2:
#        found_2_addrs.append(address_name+'  $$  '+str(local_results[0])+'  $$  '+str(local_results[1]))



# path = '/Users/meirlen/Desktop/bot/dataset/test/alem_data/orgs_result_street.txt'
# add_data_to_txt('Not found',path)
# for item in not_found_addrs:
#     add_data_to_txt(item,path)


# print('FOUND 1 ADDRESS',len(found_1_addrs)) 
# add_data_to_txt('\nFOUND 1 ADDRESS',path)
# for item in found_1_addrs:
#     add_data_to_txt(item,path)


# print('FOUND 2 ADDRESS',len(found_2_addrs)) 
# add_data_to_txt('\nFOUND 2 ADDRESS',path)
# for item in found_2_addrs:
#     add_data_to_txt(item,path)


# print('NOT FOUND',len(not_found_addrs)) 
# print('1 found',len(found_1_addrs))  
# print('2 found',len(found_2_addrs))      
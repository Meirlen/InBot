import sqlite3
import textdistance
from lemmatizer import lemma,stemmer


DB_NAME = 'krg_address.db'



# SELECT Operation
def select():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from ORGANIZATION")
    
   
    result = []

    for row in cursor:
        result.append(str(row[3])+"^^"+str(row[5])+"^^"+str(row[6])+"^^"+str(row[4])+"^^"+str(row[7])+"^^"+str(row[8]))


    conn.close()
    return result


 
# SELECT Operation
def select_street():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION")
    
   
    result = []

    for row in cursor:
        result.append(str(row[2])+"^^"+str(row[5]))


    conn.close()
    return result   


# SELECT Operation
def select_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    name = name.lower()
    cursor = conn.execute("SELECT * FROM ORGANIZATION WHERE NAME LIKE '%"+name+"%' OR NAME_ORIGIN LIKE '%"+name+"%'")
    
   
    result = []

    for row in cursor:
        result.append(str(row[0])+"  "+str(row[6])+"  "+str(row[7]))


    conn.close()
    return result

#Levenshtein distance
def myFunc(e):
  return e['dist']


import re
def search_by_levenshtein_distance(name,search_result):
    
    name = re.sub(r'[^\w]', ' ', name.strip().lower())
    name = stemmer(name)

    print(name)

    result = []

    for item in search_result:
         stem_name = item.split("^^")[0]
         dist = textdistance.levenshtein.distance(name, stem_name)
         if dist <=1:
             result.append({'response': item, 'dist': dist})
             if dist == 0:
                 result.sort(key=myFunc) 
                 return result

    result.sort(key=myFunc) 
    return result


# print((search_by_levenshtein_distance('алеханова',select_street())))
# print(select_by_name('цум'))


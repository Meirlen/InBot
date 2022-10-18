
# HELPER -----------------------------------------------------------------------------
# LOCAL DB USERS OPERATIONS

import sqlite3
from nltk.stem import SnowballStemmer



DB_NAME = 'krg_address.db'

def is_auth_user(user_id):
    user_id = str(user_id)
    if len(search(user_id)) > 0:
        return search(user_id)[0]
    else:
        return None


def insert_new_user(name, user_id, phone_number, platform,status = 'free',message = None,order_id = None):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO USERS (NAME,USER_ID,PHONE_NUMBER,PLATPHORM,STATUS,MESSAGE,ORDER_ID) \
      VALUES (?, ?, ?, ?, ?, ?, ?)", (name, user_id, phone_number, platform,status,message,order_id))
    conn.commit()
    print("New user successfully added")
    conn.close()




def search(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from USERS WHERE USER_ID = '%s'" % user_id)

    result = []

    for row in cursor:
        result.append(str(row[3]))

    conn.close()
    return result



def search_user_by_phone_number(phone_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from USERS WHERE PHONE_NUMBER = '%s'" % phone_number)

    result = []

    for row in cursor:
        result.append(str(row[2])+'&&'+str(row[5])+'&&'+str(row[6])+'&&'+str(row[4]))

    conn.close()
    return result


def get_order_id(phone_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from USERS WHERE PHONE_NUMBER = '%s'" % phone_number)

    result = []

    for row in cursor:
        result.append(str(row[7]))

    conn.close()
    return result   


def update_status(tracker,status,message = None):

    chat_id = tracker.get_slot('chat_id')

    print('Chat_id_1: '+ str(chat_id))
    if chat_id != None:
        conn = sqlite3.connect(DB_NAME)

        conn.execute('''UPDATE USERS SET STATUS = ?, MESSAGE = ? WHERE USER_ID = ?''', (status,message,chat_id))

        conn.commit()
        print ("Status updated 1 :"+str(status))

        conn.close()



def update_order_id(tracker,order_id):

    chat_id = tracker.get_slot('chat_id')
  
    print('Chat_id'+ str(chat_id))
    if chat_id != None:
        conn = sqlite3.connect(DB_NAME)
        conn.execute('''UPDATE USERS SET ORDER_ID = ? WHERE USER_ID = ?''', (order_id,chat_id))
        conn.commit()
        print ("order_id updated :"+str(order_id))
        conn.close()



        
def update_status_by_admin(chat_id,status,message = None):

    print('Chat_id'+ str(chat_id))
    if chat_id != None:
        conn = sqlite3.connect(DB_NAME)

        conn.execute('''UPDATE USERS SET STATUS = ?, MESSAGE = ? WHERE USER_ID = ?''', (status, message,chat_id))

        conn.commit()
        print ("Status updated :"+str(status))

        conn.close()        






# LOCAL DB LOCATIONS OPERATIONS

def select():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION")

    result = []

    for row in cursor:
        result.append(str(row[2])+"^^"+str(row[5])+"^^"+str(row[4])+"^^"+str(row[0])+"^^"+str(row[1])+"^^"+str(row[7])+"^^"+str(row[8]))

    conn.close()
    return result


def select_orgs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from ORGANIZATION")

    result = []

    for row in cursor:
        result.append(str(row[3])+"^^"+str(row[6])+"^^"+str(row[7]) +
                      "^^"+str(row[5])+"^^"+str(row[8])+"^^"+str(row[9])+"^^"+str(row[0])+"^^"+str(row[1])+"^^"+str(row[11])+"^^"+str(row[10]))


    conn.close()
    return result


def search_orgs(name):
    stem_name = stemmer(name)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from ORGANIZATION WHERE STEMMA = '%s'" % stem_name)
     
    result = []

    for row in cursor:
        result.append(str(row[3])+"^^"+str(row[6])+"^^"+str(row[7]) +
                      "^^"+str(row[5])+"^^"+str(row[8])+"^^"+str(row[9]))

    conn.close()
    return result


def stemmer(text):
    stemmer = SnowballStemmer("russian")
    return stemmer.stem(text)

# Levenshtein distance
import textdistance
import re


def myFunc(e):
    return e['dist']



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
        if len(array_res) == 10: # from_orgs
             source_data = 'org'
        else: # from_loc
            source_data = 'location'

        dist = textdistance.levenshtein.distance(name, stem_name)

        
        if name == stem_name:
            result.append({'response': item, 'dist': dist , 'source': source_data })
            if dist == 0:
                result.sort(key=myFunc)
                return result

    result.sort(key=myFunc)
    return result




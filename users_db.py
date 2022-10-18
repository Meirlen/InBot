import sqlite3



DB_NAME = 'krg_address.db'


# Create table
def create_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''CREATE TABLE USERS
         (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         NAME        TEXT    NOT NULL,
         USER_ID      TEXT    NOT NULL,
         PHONE_NUMBER      TEXT    NOT NULL,
         PLATPHORM       TEXT    NOT NULL,
         STATUS   DEFAULT "free"  NOT NULL,
         MESSAGE       TEXT ,
         ORDER_ID       TEXT 
         );''')

    print("Table created successfully")
    conn.close()


# INSERT Operation
def insert_user(name, user_id, phone_number, platform,status,message):

    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO USERS (NAME,USER_ID,PHONE_NUMBER,PLATPHORM,STATUS,MESSAGE) \
      VALUES (?, ?, ?, ?, ?, ?)", (name, user_id, phone_number, platform,status,message))
    conn.commit()
    print("Records created successfully")
    conn.close()

# DELETE table


def search(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from USERS WHERE USER_ID = '%s'" % user_id)

    result = []

    for row in cursor:
        result.append(str(row[3]))

    conn.close()
    return result


def show_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from USERS ")

    result = []

    for row in cursor:
        print(row)
        result.append(str(row))

    conn.close()
    print('Total users: ', len(result))
    return result


def drop_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DROP TABLE USERS")
    conn.commit()


def is_auth_user(user_id):
    if len(search(user_id)) > 0:
        return search(user_id)[0]
    else:
        return None


# UPDATE Operation
def update_status(chat_id,status):
    conn = sqlite3.connect(DB_NAME)

    conn.execute('''UPDATE USERS SET STATUS = ? WHERE ID = ?''', (status, chat_id))

    conn.commit()
    print ("Status updated :", conn.total_changes)

    conn.close()

# UPDATE Operation
def update_all_status(status):
    conn = sqlite3.connect(DB_NAME)

    conn.execute("UPDATE USERS SET STATUS = 'free' , MESSAGE = 'NULL' , ORDER_ID = 'NULL' ")

    conn.commit()
    print ("Status updated :", conn.total_changes)

    conn.close()

def search_user_by_phone_number(phone_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from USERS WHERE PHONE_NUMBER = '%s'" % phone_number)

    result = []

    for row in cursor:
        result.append(str(row[2])+'&&'+str(row[5])+'&&'+str(row[6]))

    conn.close()
    return result

def delete_user_by_phone_number(phone_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("DELETE  from USERS WHERE ID = '%s'" % phone_number)
    conn.commit()
    print ("User deleted :", conn.total_changes)

    conn.close()
 
# print(is_auth_user('348991'))

# drop_table()
# create_table()
# delete_user_by_phone_number('98')
# # update_all_status('free')
# # update_status("95",'car_arrived')

# # insert_user('indira', '7087550160', '+77087550160', 'whatsapp','free',None)
show_table()
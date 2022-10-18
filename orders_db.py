import sqlite3
from actions.app_constans import *
DB_NAME = 'krg_address.db'
from dataclasses import dataclass


@dataclass
class Template:
    title: str
    description: str


# Create a Table
def create_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''CREATE TABLE ORDERS
         (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         FROM_ADDRESS    TEXT    NOT NULL,
         TO_ADDRESS      TEXT    NOT NULL,
         FROM_AREA       TEXT    NOT NULL,
         TO_AREA        INT     NOT NULL,
         PRICE_TRIP    TEXT,
         ID_USER        TEXT    NOT NULL);''')

    print ("Table created successfully")
    conn.close()


def drop_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DROP TABLE ORDERS")
    conn.commit()


# INSERT Operation
def insert_new_order(from_address,to_address,price_trip,id_user):

    res = select_by_from_and_to_address(from_address,to_address,id_user)
    if len(res) == 0:
        conn = sqlite3.connect(DB_NAME)
        from_area = "Empty"
        to_area = "Empty"
        conn.execute("INSERT INTO ORDERS (FROM_ADDRESS,TO_ADDRESS,FROM_AREA,TO_AREA,PRICE_TRIP,ID_USER) \
        VALUES (?, ?, ?,?,?, ?)",(from_address,to_address,from_area,to_area,price_trip,id_user))
        conn.commit()
        print ("Order created successfully")
        conn.close()  


def select_by_from_and_to_address(from_a,to_a,user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from ORDERS WHERE FROM_ADDRESS = ? AND TO_ADDRESS = ? AND ID_USER = ? ",(from_a,to_a,user_id))
    
    result = []

    for row in cursor:
        order_id = str(row[0])
        from_address = str(row[1])
        to_address = str(row[2])
        result.append(from_address)
        
    conn.close()
    return result


# SELECT Operation
def get_templates(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from ORDERS WHERE ID_USER = '%s' ORDER BY ID DESC LIMIT 6" % user_id)
    
    result = []

    for row in cursor:
        order_id = str(row[0])
        from_address = str(row[1])
        to_address = str(row[2])
        template = from_address
        if to_address.lower() != "str":
           template = from_address+" "+to_address+"$"+str(order_id)

           template = template
           template = template
           result.append(template)
        
    conn.close()




    result = set(result)
    result = list(result)

    templates = []

    for index in range(len(result)): 
        index =index+1
        item = result[index-1]
        print(item)
        part_1 = item.split('$')[0]
        part_2= item.split('$')[1]
        
        order_id = TEMPLATE_START_TEXT +str(part_2)
        desc = str(part_1) 
        # desc = "Чтобы создать новый заказ вы можете просто написать адресс.  адресс  адресс jjjnjn "

        title = order_id + str(result[index-1]) 
        if len(title)>22:
           title = title[:22]+'..'

        if len(desc)>70:
           desc = desc[:70]+'..'

        template = Template(order_id,desc)
        templates.append(template)
        # print(template)


    return templates





# SELECT Operation
def get_template_by_position(order_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from ORDERS WHERE ID = '%s' " % order_id)
    
    result = []

    for row in cursor:
        template = str(row[1])+ "$" + str(row[2])+ "$" + str(row[5])
        template = template
        template = template
        result.append(template)
        
    conn.close()

    return result




#     result = set(result)
#     result = list(result)


#     for index in range(len(result)): 
#         index = index+1
#         if position == index:
#            return result[index-1]


#     return None


# def drop_table():
#     conn = sqlite3.connect(DB_NAME)
#     conn.execute("DROP TABLE ORDERS")
#     conn.commit()    

# insert_new_order("абая 89","муканова",'юг',"майкудук",'77774857133')
# print(get_templates('77774857133'))
# # drop_table()
# drop_table()
# create_table()

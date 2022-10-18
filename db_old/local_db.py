from email.headerregistry import Address
from operator import itruediv
import sqlite3

from places_yandex import search_place
DB_NAME = 'krg_address.db'
import sys
sys.path.append('../')





# TYPE: 
# 0 - улица многоэтажка 
# 1 - улица частный сектор 
# 2 - район(майкудук, пришахтиск)
# 3 - исключения(exception) например: аэропорт
 

# Create db
def create_db():
    conn = sqlite3.connect(DB_NAME)
    conn.close()
    print("Opened database successfully")


# Create a Table
def create_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''CREATE TABLE LOCATION
         (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         NAME        TEXT    NOT NULL,
         STEMMA      TEXT    NOT NULL,
         LEMMA       TEXT    NOT NULL,
         TYPE        INT     NOT NULL,
         AREA        TEXT    NOT NULL);''')

    print ("Table created successfully")
    conn.close()


# TYPE: 0 - street, 1 - organiztion


# SELECT Operation
def select_by_type(name):
    stem_name = stemmer(name)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION WHERE TYPE = '%s'" % stem_name)
    
    result = []

    for row in cursor:
        print(row[1])
        result.append(str(row[1])+"^^"+str(row[5])+"^^"+str(row[6]))

    conn.close()
    return result

def select_by_id(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION WHERE ID = '%s'" % id)
    
    result = []

    for row in cursor:
        print(row[1])
        result.append(str(row[1])+"^^"+str(row[5])+"^^"+str(row[6]))

    conn.close()
    return result

# SELECT Operation
def select(name):
    stem_name = stemmer(name)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION WHERE STEMMA = '%s'" % stem_name)
    
    result = []

    for row in cursor:
        print('id: ', row[0],'area:', row[5])
        result.append(str(row[1])+"^^"+str(row[5]))

    conn.close()
    return result


def select_by_zone(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION WHERE AREA == '%s' " % name)
    
    result = []

    for row in cursor:
        name = row[1]
        type = row[4]
        if type == 0 and len(name)>3: # only streets
            user_id = row[0]
            lat = row[7]
            lng = row[8]
            print('id: ', row[0],'name: ', row[1],' coord:',lat,lng)
            line = str(user_id) +":" + str(name) +":"+str(lat)+":" +str(lng)
            result.append(str(row[1])+"^^"+str(row[5]))

          

    conn.close()

    print('Count: ',len(result))
    return result



def update_coord_by_zone(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION WHERE AREA = '%s' " % name)
    
    result = []

    for row in cursor:
        name = row[1]
        type = row[4]
        if type == 0 and len(name)>3: # only streets
            user_id = row[0]
            print('id: ', row[0],'name: ', row[1])
            result.append(str(row[1])+"^^"+str(row[5]))

            # get coordinates by yandex api
            res = search_place(name)
            if len(res) > 0:
                point = res[0]['geometry']['coordinates']
                lat = point[1]
                lng = point[0]
                line = str(user_id) +":" +str(lat)+":" +str(lng)
                add_data_to_txt(line,'/Users/meirlen/Desktop/bot/dataset/street_coords.txt')
                print(point)
                # update_coordinates(id,lat,lng)
            else:
                print(name, ' search result None')

    conn.close()

    print('Count: ',len(result))
    return result

from lemmatizer import lemma,stemmer
# INSERT Operation
def insert(name,type,area):
    conn = sqlite3.connect(DB_NAME)
    name = name.lower()
    lemma_name = lemma(name)
    stem_name = stemmer(name)


    conn.execute("INSERT INTO LOCATION (NAME,STEMMA,LEMMA,TYPE,AREA) \
      VALUES (?, ?, ?,?, ?)",(name,stem_name,lemma_name,type,area))
    conn.commit()
    print ("Records created successfully")
    conn.close()  




# DELETE Operation
def add_colmn():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("ALTER TABLE LOCATION ADD COLUMN LAT TEXT")
    conn.commit()
    print ("Column added")
    conn.close()





# UPDATE Operation
def update_type(id,type):
    conn = sqlite3.connect(DB_NAME)

    conn.execute('''UPDATE LOCATION SET TYPE = ? WHERE ID = ?''', (type, id))

    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)

    conn.close()

# UPDATE Operation
def update_area(id,area):
    conn = sqlite3.connect(DB_NAME)

    conn.execute('''UPDATE LOCATION SET AREA = ? WHERE ID = ?''', (area, id))

    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)

    conn.close()

def update_coordinates(id,lat,lng):
    conn = sqlite3.connect(DB_NAME)

    conn.execute('''UPDATE LOCATION SET LAT = ?,LNG = ?  WHERE ID = ?''', (lat,lng, id))

    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)

    conn.close()

def update_coordinates_all(area,lat,lng):
    conn = sqlite3.connect(DB_NAME)

    conn.execute('''UPDATE LOCATION SET LAT = ?,LNG = ?  WHERE AREA = ?''', (lat,lng, area))

    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)

    conn.close()
# UPDATE Operation
def update_area_by_area(area,new_area):
    conn = sqlite3.connect(DB_NAME)

    conn.execute('''UPDATE LOCATION SET AREA = ? WHERE AREA = ?''', (new_area,area))

    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)

    conn.close()

def update_coords():
     res = read_data_from_txt('/Users/meirlen/Desktop/bot/dataset/street_coords.txt')
     for item in res:
         id,lat,lng = item.split(':')
         update_coordinates(id,lat,lng)


# UPDATE Operation
def update_name(id,name):
    conn = sqlite3.connect(DB_NAME)

    conn.execute('''UPDATE LOCATION SET NAME = ? , STEMMA = ? , LEMMA = ? WHERE ID = ?''', (name,name,name,id))

    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)

    conn.close()

# DELETE Operation
def delete_by_id(id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE from LOCATION where ID = "+id+";")
    conn.commit()
    print ("Total number of rows deleted :", conn.total_changes)

    conn.close()


def add_data_to_txt(contents,file_path):
        file = open(file_path,"a")
        file.writelines(contents+'\n')
        file.close()  


def read_data_from_txt(file_path):
     with open(file_path) as f:
           lines = f.readlines()
     result = []
     for line in lines:
         result.append(line.strip())
     print(len(result)) 
     return  result        



# add_colmn()


# update_info(38,1)
#create_db()
#create_table()

# delete_by_id('233')
# print(select("16"))
# insert('кривогуза',0,'город')


#  areas = ['майкудук','город','пришахтинск','михайловка','федоровка','юг']
# areas = [ 'Саран', 'Темиртау','Дубовка','Кокпекти', 'Актас', 'Шахтинск','Шахан','Доскей','Ботакара','Уштобе']#'Абай',
# areas = [ 'астана', 'алматы','жезказган','каркаралы']

# for area in areas:
#     insert(area,2,area)



# update_name(557,'12')


# print(select('11'))

# 
def unique_zone_names():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT DISTINCT AREA from LOCATION")
    
    result = []

    for row in cursor:
        print('id: ', row)
        # result.append(str(row[1])+"^^"+str(row[5]))

    conn.close()
    return result




class Address:
    lat: str
    lng: str
    name: str 

adresses = []
adresses.append(Address())

# нижний м 49.89326374665135, 73.19118547707303
# 18 мкр 49.87010601031509, 73.18948031268003
# архитектурная 49.88009297542908, 73.18770534696638
# прихан 49.90544402884051, 73.08096041598948
# верхний 49.8515380558234, 73.18306450898804

# # низ
# update_coordinates(212,49.89326374665135, 73.19118547707303)
# update_coordinates(264,49.89326374665135, 73.19118547707303)
# update_coordinates(436,49.89326374665135, 73.19118547707303)
# update_coordinates(329,49.89326374665135, 73.19118547707303)
# update_coordinates(105,49.89326374665135, 73.19118547707303)
# update_coordinates(557,49.89326374665135, 73.19118547707303)

# # # середина
# update_coordinates(556,49.87010601031509, 73.18948031268003)

# # # верх
# update_coordinates(107,49.8515380558234, 73.18306450898804)
# update_coordinates(266,49.8515380558234, 73.18306450898804)
# update_coordinates(257,49.8515380558234, 73.18306450898804)

# # город
# update_coordinates(1,49.8192682588708, 73.09338838803014)
# update_coordinates(7,49.8192682588708, 73.09338838803014)
# update_coordinates(80,49.8192682588708, 73.09338838803014)
# update_coordinates(82,49.8192682588708, 73.09338838803014)
# update_coordinates(106,None, None)
# update_coordinates(143,49.8192682588708, 73.09338838803014)
# update_coordinates(316,49.8192682588708, 73.09338838803014)
# update_coordinates(484,49.8192682588708, 73.09338838803014)
# update_coordinates(316,49.8192682588708, 73.09338838803014)
# update_coordinates(316,49.8192682588708, 73.09338838803014)



# select_by_id('54')
# # update_coordinates(263,None,None)

# update_area_by_area('майкудук\n','майкудук')
# select_by_type('0')
# select_by_zone('майкудук\n')
# update_area_by_area('юг\n','юг')
# update_coordinates_all('юг',49.7738311820074,73.1317996134278)
# select_by_zone('юг')

# update_coords()
# unique_zone_names()
   
# select_by_zone('город\n')
# select('11')

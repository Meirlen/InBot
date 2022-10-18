import sqlite3
from unicodedata import category

DB_NAME = 'krg_address.db'

# TYPE: 
# 0 - улица многоэтажка 
# 1 - улица частный сектор 
# 2 - район(майкудук, пришахтиск)


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
def select(name):
    stem_name = stemmer(name)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from ORGANIZATION WHERE STEMMA = '%s'" % stem_name)
    
    result = []

    for row in cursor:
        result.append(str(row[3])+"^^"+str(row[5]))

    conn.close()
    return result



from lemmatizer import lemma,stemmer
# INSERT Operation
def insert(name,address,area,lat,lng):
    category = 'Default'
    conn = sqlite3.connect(DB_NAME)
    name = name.lower()
    lemma_name = lemma(name)
    stem_name = stemmer(name)


    conn.execute("INSERT INTO ORGANIZATION (NAME_ORIGIN,NAME,STEMMA,LEMMA,AREA,CATEGORY,ADDRESS,LAT,LNG) \
      VALUES (?, ?, ?,?,?, ?,?,?,?)",(name,name,stem_name,lemma_name,area,category,address,lat,lng))
    conn.commit()
    print ("Records created successfully")
    conn.close()  



# DELETE Operation
def add_colmn():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("ALTER TABLE LOCATION ADD COLUMN SYNONYM TEXT")
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
def update_name(id,name):
    conn = sqlite3.connect(DB_NAME)

    conn.execute('''UPDATE LOCATION SET NAME = ? , STEMMA = ? , LEMMA = ? WHERE ID = ?''', (name,name,name,id))

    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)

    conn.close()


# DELETE Operation
def delete_by_id(id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE from ORGANIZATION where ID = "+id+";")
    conn.commit()
    print ("Total number of rows deleted :", conn.total_changes)

    conn.close()



def delete_by_id_compare(id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE from ORGANIZATION where ID > "+id+";")
    conn.commit()
    print ("Total number of rows deleted :", conn.total_changes)

    conn.close()

# чч
# add_colmn()

# delete_by_id_compare('3305')
# delete_by_id('3398')

# insert('арбат','проспект Бухар-Жырау, 55/2','город','49.802798','73.086595')

# update_info(38,1)
#create_db()
#create_table()

print(select("ая"))

#  areas = ['майкудук','город','пришахтинск','михайловка','федоровка','юг']
# areas = [ 'Саран', 'Темиртау','Дубовка','Кокпекти', 'Актас', 'Шахтинск','Шахан','Доскей','Ботакара','Уштобе']#'Абай',
# areas = [ 'астана', 'алматы','жезказган','каркаралы']

# for area in areas:
#     insert(area,2,area)

# insert('астана',2,'алматы')


# update_name(557,'12')


# print(select('11'))

# 
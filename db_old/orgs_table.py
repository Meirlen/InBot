import sqlite3
from pre_proccess import clear
DB_NAME = 'krg_address.db'



# Create db
def create_db():
    conn = sqlite3.connect(DB_NAME)
    conn.close()
    print("Opened database successfully")


# Create table
def create_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''CREATE TABLE ORGANIZATION
         (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         NAME_ORIGIN        TEXT    NOT NULL,
         NAME        TEXT    NOT NULL,
         STEMMA      TEXT    NOT NULL,
         LEMMA       TEXT    NOT NULL,
         CATEGORY       TEXT    NOT NULL,
         AREA       TEXT    NOT NULL,
         ADDRESS      TEXT    NOT NULL,
         NETWORK     TEXT  ,
         INFO        TEXT  ,
         LAT         FLOAT,
         LNG         FLOAT

         
          );''')

    print ("Table created successfully")
    conn.close()




# SELECT Operation
def select(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from ORGANIZATION WHERE NAME = '%s'" % name)
    
    result = []

    for row in cursor:
        print(row)
        result.append(str(row[1])+"^^"+str(row[5])+"^^"+str(row[6])+"^^"+str(row[4])+"^^"+str(row[7])+"^^"+str(row[8]))

    conn.close()
    return result



from lemmatizer import lemma,stemmer
# INSERT Operation
def insert(name,area,category,address,network,info,lat,lng):
    conn = sqlite3.connect(DB_NAME)

    lemma_name = lemma(name)
    stem_name = stemmer(name)


    conn.execute("INSERT INTO ORGANIZATION (NAME_ORIGIN,NAME,STEMMA,LEMMA,CATEGORY,AREA,ADDRESS,NETWORK,INFO,LAT,LNG) \
      VALUES (?, ?, ?, ?,?, ?,?,?,?,?,?)",(name,name,stem_name,lemma_name,category,area,address,network,info,lat,lng))
    conn.commit()
    print ("Records created successfully")
    conn.close()  


# DELETE 
def delete(id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute('DELETE from ORGANIZATION WHERE ID = '+str(id))
    conn.commit()
    print ("Total number of rows deleted :", conn.total_changes)
    conn.close()


# DELETE table
def drop_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DROP TABLE ORGANIZATION")
    conn.commit()


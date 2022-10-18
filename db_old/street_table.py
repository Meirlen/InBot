import sqlite3

DB_NAME = 'krg_address.db'



# Create db
def create_db():
    conn = sqlite3.connect(DB_NAME)
    conn.close()
    print("Opened database successfully")


# Create table
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


# SELECT 
def select(name):
    stem_name = stemmer(name)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION WHERE STEMMA = '%s'" % stem_name)
    
    result = []

    for row in cursor:
        result.append(str(row[1])+"^^"+str(row[5]))

    conn.close()
    return result


# SELECT 
def select_has_synonym():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * from LOCATION ")
    
    result = []

    for row in cursor:
        synonym = row[6]
        if synonym != None:
            result.append(str(row[1])+"^^"+synonym)
       
        

    conn.close()
    return result

from lemmatizer import lemma,stemmer
# INSERT Operation
def insert(name,type,area):
    conn = sqlite3.connect(DB_NAME)

    lemma_name = lemma(name)
    stem_name = stemmer(name)


    conn.execute("INSERT INTO LOCATION (NAME,STEMMA,LEMMA,TYPE,AREA) \
      VALUES (?, ?, ?,?, ?)",(name,stem_name,lemma_name,type,area))
    conn.commit()
    print ("Records created successfully")
    conn.close()  




# UPDATE Operation
def update_info(id,type):
    conn = sqlite3.connect(DB_NAME)

    conn.execute('''UPDATE LOCATION SET TYPE = ? WHERE ID = ?''', (type, id))

    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)

    conn.close()




# UPDATE Operation
def update_synonym(id,synonyms):
    conn = sqlite3.connect(DB_NAME)

    conn.execute('''UPDATE LOCATION SET SYNONYM = ? WHERE ID = ?''', (synonyms, id))

    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)

    conn.close()



# select_has_synonym()
# update_synonym(316,'нуркена абдирова, нуркена')
# 
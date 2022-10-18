import sqlite3



DB_NAME = 'krg_address.db'


# returns a list of table names available in an SQLite3 database.
def table_list():
    con = sqlite3.connect(DB_NAME)
    cursor = con.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

table_list()
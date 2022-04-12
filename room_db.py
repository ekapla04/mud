import sqlite3
import csv


def connect():
    # connect to database
    conn = sqlite3.connect("rooms.db")

    # create cursor object to send SQL statements to db
    cursor = conn.cursor()

    # i believe associating primary key with username means only one person 
        # can have any given username
    createTables(conn, cursor)
    importData(conn,cursor)



def createTables(conn, cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS room \
                    (id TEXT, \
                    name TEXT, \
                    description TEXT)")

def importData(conn, cursor):
    print("in import data")
    with open('room.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['id'], i['name'], i['description']) for i in dr]
    # print("in import data")
    cursor.executemany("INSERT INTO room (id, name, description) VALUES (?, ?, ?);", to_db)
    rows = cursor.execute("SELECT * FROM room")
    print(rows)

    # conn.commit()
    # conn.close() 

connect()

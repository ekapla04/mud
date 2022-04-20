import sqlite3
import csv

import sqlite3

from tables import Description

class RoomDatabase(object):

    def __init__(self):
        '''initialize db class variables'''
        self.connection = sqlite3.connect("rooms.db")
        self.cur = self.connection.cursor()
        self.create_table()
        # print("table created")


    def close(self):
        '''close sqlite3 connection'''
        self.connection.close()


    def execute(self, new_data):
        '''execute a row of data to current cursor'''
        self.cur.execute(new_data)


    def executemany(self, many_new_data):
        '''replace database data. only to be used internally
           to update existing entries, otherwise will create new entry with 
           data...'''
        # self.create_table()
        self.cur.executemany('REPLACE INTO rooms VALUES(?, ?, ?, ?, ?)', \
                            (many_new_data,))
    

    def add_room(self,data):
        '''attempt to add a single room to the database'''
        uui, name, description, exits, characters = data
        # print("data: " + str(data))
        boolean, result = self.in_table((uui, name))
        # print("boolean: " + str(boolean))
        if (boolean == False):
            print("result is false")
            self.cur.execute("INSERT INTO rooms VALUES \
                              (?, ?, ?, ?, ?)", (uui, name, description, \
                                                    exits, characters))
            # print("room added!")
        else:
            print("already in table!")
    

    def in_table(self, data):
        '''check for username/password match in database'''
        uui, name = data
        self.cur.execute('SELECT * from rooms WHERE \
                                   uui="%s" AND name="%s"'\
                                   %(uui,name))
        result = self.cur.fetchall()
        if(len(result) > 0):
            print("len > 0")
            return True, result
        else:
            print("room " + str(uui) + ", " + str(name) + " not in table")
            return False, "None"

    def create_table(self):
        '''create a database table if it does not exist already'''
        # this isn't uuieal in terms of storing lists
        # must be stored as a single string with words separated by 
        # commas... sqlite3 doesnt have ability to store lists/tuples 
        # in a column. uui stands for universally unique uuientifier
        self.cur.execute("CREATE TABLE IF NOT EXISTS rooms \
                                                    (uui TEXT PRIMARY KEY, \
                                                    name TEXT, \
                                                    description TEXT, \
                                                    exits TEXT, \
                                                    characters TEXT)")
    

    def parse_information(self, data, row):
        '''returns either exits or characters in tuple format
           using uui/name for character/exit look up'''
        exists,result = self.in_table(data) 
        # print("result:" + str(result))
        # print(exists)
        if (exists == True and row == "exits"):
            items = result[0][3].split(", ")
            return items
        elif (exists == True and row == "characters"):
            items = result[0][4].split(", ")
            return items
        else:
            print("cannot retrieve data because room does not exist")

    def import_data(self, filename):
        self.cur.execute(LOAD DATA INFILE 'c:/tmp/discounts.csv' 
                        INTO TABLE discounts 
                        FIELDS TERMINATED BY ',' 
                        ENCLOSED BY '"'
                        LINES TERMINATED BY '\n'
                        IGNORE 1 ROWS;
        # with open(filename,'r') as fin: # `with` statement available in 2.5+
        # # csv.DictReader uses first line in file for column headings by default
        #     dr = csv.DictReader(fin) # comma is default delimiter
        #     for i in dr:
        #         uui = i['uui']
        #         name = i['name']
        #         description = i['description']
        #         exits = i['exits']
        #         characters = i['characters']
        #     # to_db = [(i['uui'], i['name'], i['description'], \
        #     #           i['exits'], i['characters'],) for i in dr]
        # self.add_room((uui, name, description, exits, characters))
    

    def commit(self):
        '''commit changes to database'''
        self.connection.commit()



# def importData(conn, cursor):
#     print("in import data")
#     with open('room.csv','r') as fin: # `with` statement available in 2.5+
#     # csv.DictReader uses first line in file for column headings by default
#         dr = csv.DictReader(fin) # comma is default delimiter
#         to_db = [(i['uui'], i['name'], i['description']) for i in dr]
#     # print("in import data")
#     cursor.executemany("INSERT INTO room (uui, name, description) VALUES (?, ?, ?);", to_db)
#     rows = cursor.execute("SELECT * FROM room")
#     print(rows)

#     # conn.commit()
#     # conn.close() 

# connect()

import sqlite3
import csv
from src.room import Room
from src.character import Character
import re


class Database(object):

############# DATABASE INITIALIZATION/CREATION ##############

    def __init__(self, db_name):
        '''initialize db class variables'''
        self.connection = sqlite3.connect(db_name)
        self.cur = self.connection.cursor()

        if (db_name == "users.db"):
            self.create_userDB()
        elif (db_name == "rooms.db"):
            self.create_roomDB()

    
    def create_roomDB(self):
        '''create a room database table if it does not exist already'''
        self.cur.execute("CREATE TABLE IF NOT EXISTS rooms \
                                                    (uui TEXT PRIMARY KEY, \
                                                    name TEXT, \
                                                    description TEXT, \
                                                    exits TEXT, \
                                                    characters TEXT)")
        
    def create_userDB(self):
        '''create a user database table if it does not exist already'''
        self.cur.execute("CREATE TABLE IF NOT EXISTS users \
                                            (username TEXT PRIMARY KEY, \
                                            password TEXT, \
                                            description TEXT, \
                                            location TEXT, \
                                            inventory TEXT, \
                                            hp INT)")
    

    # i dont think this will work how we want it to... no way to store
    # character/room objects in CSV...
    def import_data(self, filename):
        with open(filename,'r') as fin:
            dr = csv.DictReader(fin) # comma is default delimiter
            for i in dr:
                uui = i['uui']
                name = i['name']
                description = i['description']
                exits = i['exits']
                characters = i['characters']
        self.add_room((uui, name, description, exits, characters))
    

    def commit(self):
        '''commit changes to database'''
        self.connection.commit()


    def close(self):
        '''close sqlite3 connection'''
        self.connection.close()


    def execute(self, new_data):
        '''execute a row of data to current cursor'''
        self.cur.execute(new_data)

#############################################################

################### UPDATE/ADD DATA TO DB ###################

    def execute_rooms(self, many_new_data):
        '''replace room database data. only to be used internally
           to update existing entries, otherwise will create new entry with 
           data...'''
        self.cur.executemany('REPLACE INTO rooms VALUES(?, ?, ?, ?, ?)', \
                            (many_new_data,))


    def execute_users(self, many_new_data):
        '''replace user database data. only to be used internally
        to update existing entries, otherwise will create new entry with 
        data...'''
        self.cur.executemany('REPLACE INTO users VALUES(?, ?, ?, ?, ?, ?)', \
                    (many_new_data,))
    

    def add_room(self,data):
        '''attempt to add a single room to the room database'''
        uui, name, description, exits, characters = data
        boolean, result = self.in_rooms((uui, name))
        if (boolean == False):
            self.cur.execute("INSERT INTO rooms VALUES \
                              (?, ?, ?, ?, ?)", (uui, name, description, \
                                                    exits, characters))
            status = "success"
        else:
            status = "Error: room [" + str(uui) + ", " + \
                      str(name) + "] already in table"
    
        return status
    

    def add_user(self,data):
        '''attempt to add a single user to the database'''
        print('hello')
        username, pswd, desc, location, inventory, hp = data
        if (self.in_users(username) == False):
            print("false")
            self.cur.execute("INSERT INTO users (username, password, \
                                                description, location, \
                                                inventory, hp) VALUES \
                              (?,?,?,?,?,?)", (username, pswd, desc, location, \
                                               inventory, hp))
            status = "success"
        else:
            status = "Error: character [" + str(username) + ", " + \
                      str(pswd) + "] already in table"
    
        return status
    
#############################################################

################ CHECK FOR ROW/CONTENTS IN DB ################

    def in_rooms(self, uui):
        '''check for username/password match in database'''
        self.cur.execute('SELECT * from rooms WHERE \
                                   uui="%s"'\
                                   %(uui,))
        result = self.cur.fetchall()
        if(len(result) > 0):
            return True, result
        else:
            return False, ("Error: room [" + str(uui) + "] not in table")
    
    def in_users(self, username):
        '''check for username match in database'''
    
        self.cur.execute('SELECT * from users WHERE \
                                    username="%s"'\
                                    %(username,))
        result = self.cur.fetchall()
        if(len(result) > 0):
            return True, result
        else:
            return False, ("Error: character [" + str(username) + \
                          "] not in table")
    
#############################################################


    def parse_room_lists(self, data, row):
        '''returns either exits or characters in tuple format
           using uui/name for character/exit look up'''
        exists,result = self.in_rooms(data) 
        if (exists == True and row == "exits"):
            items = result[0][3].split(", ")
            return items
        elif (exists == True and row == "characters"):
            items = result[0][4].split(", ")
            return items
        else:
            return result


    def load_room(self, room):
        '''load room object into database'''
        uui = room.getUniqueID() 

        name = room.getDisplayName()

        description = room.getDescription()

        exits = []
        exit_dict = room.getExits()
        for val in exit_dict.values():
            unique_id = val.getUniqueID()
            exits.append(str(unique_id))

        characters = []
        char_dict = room.getCharacters()

        # dont need password to ID character because username is unique
        for key in char_dict.keys():
            char_name = key.get_name()
            characters.append("[" + char_name + "]")

        self.add_room((uui, name, description, \
                           str(exits), str(characters)))

    
    def retrieve_room(self, data):
        boolean, row = self.in_rooms(data)
        print(row)
        if boolean == True:
            uui = row[0][0]
            name = row[0][1]
            description = row[0][2]
            room = Room(uui, name, description)
            
            
            # exits = self.retrieve_room((row[0][3]).strip("[]").strip("''"))
            # print(exits)
            # this is where cycle continues... for exit in exits, retrieve room
                # MUST be a character in a room for it to exist
                # infinite loop bc one exit --> other exit --> back to og exit


            characters = self.retrieve_character(row[0][4], room)
            for character in characters:
                room.addCharacter(character)

            return room

    def retrieve_character(self, room_characters, room):

        res = re.findall(r'\[.*?\]', room_characters.strip("").strip("[]"))

        users = Database("users.db")

        characters = []

        for item in range(len(res)):
            username = res[item].strip("[]")
            boolean, result = users.in_users(username)

            if (boolean == True):
                name, password, description, \
                location, items, hp = users.retrieve_character_data(result)

                character = Character(name, password, description, location)
                for item in items:
                    # this will need to be tweaked bc need item db
                    character.addToInventory(item)
                character.updateHP(hp)

                characters.append(character)
        
        return characters
    
    
    def retrieve_character_data(self, data):
        name = data[0][0]
        password = data[0][1]
        description = data[0][2]
        location = data[0][3]
        items = data[0][4].split(", ")
        hp = data[0][5]
        
        return (name, password, description, location, items, hp)

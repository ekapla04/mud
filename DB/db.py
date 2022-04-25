import sys
sys.path.insert(0, '/h/ekapla04/comp21/mud/src')

import sqlite3
from room import Room
from character import Character
from items import Items
import re


class Database(object):

############# DATABASE INITIALIZATION/CREATION ##############

    def __init__(self, db_name):
        '''initialize db class variables'''
        self.connection = sqlite3.connect(db_name)
        self.cur = self.connection.cursor()

        if (db_name == "users.db"):
            self.create_userDB()
        if (db_name == "rooms.db"):
            self.create_roomDB()
        elif (db_name == "items.db"):
            self.create_itemsDB()

    
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

    
    def create_itemsDB(self):
        '''create a item database table if it does not exist already'''
        self.cur.execute("CREATE TABLE IF NOT EXISTS items \
                                            (name TEXT, \
                                            description TEXT, \
                                            visible TEXT, \
                                            in_possession TEXT)")
    

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
        self.commit()


    def execute_users(self, many_new_data):
        '''replace user database data. only to be used internally
        to update existing entries, otherwise will create new entry with 
        data...'''
        self.cur.executemany('REPLACE INTO users VALUES(?, ?, ?, ?, ?, ?)', \
                    (many_new_data,))
        self.commit()


    def execute_items(self, many_new_data):
        '''replace user database data. only to be used internally
        to update existing entries, otherwise will create new entry with 
        data...'''
        self.cur.executemany('REPLACE INTO items VALUES(?, ?, ?, ?)', \
                    (many_new_data,))
        self.commit()
    

    def add_room(self,data):
        '''attempt to add a single room to the room database'''
        uui, name, description, exits, characters = data
        boolean, result = self.in_rooms(uui)
        if (boolean == False):
            self.cur.execute("INSERT INTO rooms VALUES \
                              (?, ?, ?, ?, ?)", (uui, name, description, \
                                                    exits, characters))
            status = "success"
            # self.commit()
        else:
            status = "Error: room [" + str(uui) + ", " + \
                      str(name) + "] already in table"
    
        return status
    

    def add_user(self,user):
        '''attempt to add a single user to the database'''
        username = user.get_name()
        pswd = user.get_pswd()
        desc = user.get_desc()
        location = user.getLocation()
        items = user.getInventory()
        hp = user.getHP()

        inventory = ""
        for item in items:
            inventory += item.getName() + ", "

        bool, information = self.in_users(username)
        if (bool == False):
            print("false")
            self.cur.execute("INSERT INTO users (username, password, \
                                                description, location, \
                                                inventory, hp) VALUES \
                              (?,?,?,?,?,?)", (username, pswd, desc, location, \
                                               inventory, hp))
            status = "success"
            # self.commit()
        else:
            print("true")
            status = "Error: character [" + str(username) + ", " + \
                      str(pswd) + "] already in table"
    
        return status


    def add_item(self,item):
        '''attempt to add a single user to the database'''
        users = Database("users.db")
        rooms = Database("rooms.db")

        name = item.getName()
        description = item.getDescription()
        visible = item.isVisible()
        in_possession = item.inPossession()
        

        # in_rooms, room = rooms.in_rooms(in_possession)
        # in_users, user = users.in_users(in_possession)
        # if (in_rooms == False and in_users == False):
        #     print("not a valid possessor")
        # else:
        #     print("booyah")
        
        self.cur.execute("INSERT INTO items (name, description, \
                          visible, in_possession) VALUES (?,?,?,?)", \
                          (name, description, str(visible), \
                           in_possession))
        # self.commit()        
        

    def update_user_items(self, user, item_name):
        bool, result = self.in_users(user)
        print(result)
        if (result[0][4] == ""):
            item_name = item_name
        else:
            item_name = result[0][4] + ", " + item_name

        if (bool == True):
            self.cur.execute("UPDATE users SET inventory = '%s' \
                                where username = '%s'" %(item_name,user,))
        bool, result = self.in_users(user)
        print(result)

#############################################################

################ CHECK FOR ROW/CONTENTS IN DB ################

    def in_rooms(self, uui):
        '''check for room existence in database'''
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

    def in_items(self, data):
        '''check for item in database. can be in possession of a room or a
           user'''

        name, in_possession = data

        self.cur.execute('SELECT * from items WHERE name="%s" AND \
                        in_possession="%s"' %(name, in_possession,))

        result = self.cur.fetchall()
        if(len(result) > 0):
            return True, result
        else:
            return False, ("Error: item [" + str(name) + \
                          "] not in possession of " + str(in_possession))
    
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

        directions = exit_dict.keys()
        directions = list(directions)
        index = 0

        for val in exit_dict.values():
            display_name = val.getDisplayName()
            unique_id = val.getUniqueID()
            exits.append("[" + str(unique_id) + " " + str(display_name) + \
                         " " + directions[index] + "]")
            index += 1

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
        if boolean == True:
            uui = row[0][0]
            name = row[0][1]
            description = row[0][2]
            room = Room(uui, name, description)
            
            
            
            exits = self.retrieve_exits(row[0][3])
            for exit in exits:
                split = exit.split(" ")
                identifiers = str(split[0]) + " " + str(split[1])
                direction = str(split[2])
                room.addNeighbor(identifiers, direction)


            characters = self.retrieve_character(row[0][4], room)
            for character in characters:
                room.addCharacter(character)

            return room
    
    def retrieve_exits(self, room_exits):
        res = re.findall(r'\[.*?\]', room_exits.strip("").strip("[]"))

        exits = []

        for item in range(len(res)):
            exit = res[item].strip("[]")
            exits.append(exit)
        
        return exits


    def retrieve_character(self, room_characters, room):

        res = re.findall(r'\[.*?\]', room_characters.strip("").strip("[]"))

        users = Database("users.db")
        items_db = Database("items.db")

        characters = []

        for item in range(len(res)):
            username = res[item].strip("[]")
            boolean, result = users.in_users(username)

            if (boolean == True):
                name, password, description, \
                location, items, hp = users.retrieve_character_data(result)

                character = Character(name, password, description, location)
                for i in items:
                    in_items, item = items_db.in_items((i, character.get_name()))
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

    
    def return_all_rooms(self):
        self.cur.execute('SELECT * from rooms')
        db = self.cur.fetchall()

        rooms = []
        for entry in db:
            rooms.append(self.retrieve_room(entry[0]))

        return rooms

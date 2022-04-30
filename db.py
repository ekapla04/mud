# this makes it so that we can use modules held in another folder

import sqlite3
from src.room import Room
from src.character import Character
from src.items import Items
import re

# TODO:
    # write function to delete item from user inventory
    # write function to delete item from item DB
    # function to change room character is in --> location field


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
                                                    characters TEXT, \
                                                    items TEXT)")

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

    
    def delete_room(self, roomID):
        '''deletes specified room from room DB. this is primarily for testing
           purposes -- if room is deleted in game, associated players will be 
           in limbo bc not implenmeted so that they are also removed from
           existence'''

        self.cur.execute("DELETE FROM rooms where uui = '%s'" %(roomID,))
        self.commit()
    
    def delete_user_from_users(self, username):
        '''deletes specified user from users DB'''
        in_users, users_result = self.in_users(username)
        location = users_result[0][3]
        self.cur.execute("DELETE FROM users where username = '%s'" %(username,))
        self.commit()
        self.delete_user_from_room(username, location)
    
    def delete_user_from_room(self, username, uui):
        '''deletes specified user from specified room'''
        
        in_rooms, rooms_result = self.in_rooms(uui)
        username = "[" + username + "]"
        print("username: " + username)
        characters = ""
        if (in_rooms == True):
            if username in rooms_result[0][4]:
                characters = rooms_result[0][4].replace(username, "").replace(",", "")
            # print("character not in room yet")
                self.cur.execute("UPDATE rooms SET characters = '%s' \
                                    where uui = '%s'" %(characters, uui,))
                self.commit()


    
    def delete_item_from_users(self, item_name, in_possession):
        '''deletes specified item from users inventory. if item not in 
           inventory, nothing happens. if multiple items with same name, 
           all items will be deleted'''

        in_users, users_result = self.in_users(in_possession)
        users = users_result[0][4].replace(item_name, "").replace(",", "")

        if (in_users == True):
            self.cur.execute("UPDATE users SET inventory = '%s' \
                                where username = '%s'" %(users, in_possession,))

            self.commit()
    
    def delete_item_from_items(self, item, in_possession):
        self.cur.execute("DELETE FROM items where name = '%s' and \
                          in_possession = '%s'" %(item, in_possession,))
        self.commit()

    
    def change_user_room(self, username, uui):
        '''changes location of user from one room to another. updates
           user entry & updates room user logs'''
        

        in_users, user_result = self.in_users(username)

        if (in_users == True):
            self.cur.execute("UPDATE users SET location = '%s' \
                                where username = '%s'" %(uui, username,))
            self.commit()
    

    def room_swap(self, origin, destination, username):
        self.change_user_room(username, destination)
        self.delete_user_from_room(username, origin)
        self.update_room_characters(destination,username)

                
    def add_user_to_room(self, user, uui):
        print("add user to room")
        in_rooms, room_result = self.in_rooms(uui)

        if (in_rooms == True):
            users = str(room_result[0][4]) + "[" + str(user) + "]"
            print(users)
            self.cur.execute("UPDATE rooms SET characters = '%s' \
                                where uui = '%s'" %(users, uui,))
                

#############################################################

################### UPDATE/ADD DATA TO DB ###################

    def execute_rooms(self, many_new_data):
        '''replace room database data. only to be used internally
           to update existing entries, otherwise will create new entry with 
           data...'''
        self.cur.executemany('REPLACE INTO rooms VALUES(?, ?, ?, ?, ?, ?)', \
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
        '''replace items database data. only to be used internally
        to update existing entries, otherwise will create new entry with 
        data...'''
        self.cur.executemany('REPLACE INTO items VALUES(?, ?, ?, ?)', \
                    (many_new_data,))
        self.commit()
    

    def add_room(self,data):
        '''attempt to add a single room to the room database'''
        uui, name, description, exits, characters, items = data
        boolean, result = self.in_rooms(uui)

        # check if room is already in DB or not
        if (boolean == False):
            self.cur.execute("INSERT INTO rooms VALUES \
                              (?, ?, ?, ?, ?, ?)", (uui, name, description, \
                                                    exits, characters, items))
            status = "success"
            self.commit()
        else:
            status = "Error: room [" + str(uui) + ", " + \
                      str(name) + "] already in table"
    
        return status
    

    def add_user(self,user):
        '''attempt to add a single user to the database'''
        username = user.get_name()
        pswd = user.get_pswd()
        desc = user.get_desc()
        location = user.getLocation().getUniqueID()
        items = user.getInventory()
        hp = user.getHP()

        inventory = ""
        for item in items:
            inventory += item.getName() + ", "

        # check if user is already in DB or not
        bool, information = self.in_users(username)
        if (bool == False):
            self.cur.execute("INSERT INTO users (username, password, \
                                                description, location, \
                                                inventory, hp) VALUES \
                              (?,?,?,?,?,?)", (username, pswd, desc, location, \
                                               inventory, hp))
            status = "success"
            self.commit()
        else:
            status = "Error: character [" + str(username) + ", " + \
                      str(pswd) + "] already in table"
    
        return status


    def add_item(self,item):
        '''attempt to add a single item to the database'''

        name = item.getName()
        description = item.getDescription()
        visible = item.isVisible()
        in_possession = item.inPossession()
        
        # check if item is already in DB or not
        self.cur.execute("INSERT INTO items (name, description, \
                          visible, in_possession) VALUES (?,?,?,?)", \
                          (name, description, str(visible), \
                           in_possession))
        self.commit()        
        

    def update_user_items(self, user, item_name):
        '''update items in a user's inventory, will add duplicate entries'''

        bool, result = self.in_users(user)
        if (result[0][4] != ""):
            item_name = result[0][4] + ", " + item_name

        if (bool == True):
            self.cur.execute("UPDATE users SET inventory = '%s' \
                                where username = '%s'" %(item_name,user,))
            self.commit()

    
    def update_room_items(self, uui, item):
        '''update items in a room's inventory'''

        item_name = item.getName()
        bool, result = self.in_rooms(uui)
        if (result[0][5] != ""):
            item_name = result[0][5] + "[" + item_name + "]"
        
        print("item name: " + str(item_name))

        if (bool == True):
            self.cur.execute("UPDATE rooms SET items = '%s' \
                                where uui = '%s'" %(item_name,uui,))

    def update_room_characters(self, uui, character):
        '''update characters in a room'''
        in_rooms, rooms_result = self.in_rooms(uui)

        print("characters: " + str(rooms_result[0][4]))

        if character not in rooms_result[0][4]:
            characters = rooms_result[0][4] + "[" + character + "]"

            if (in_rooms == True):
                print("character not in room yet")
                self.cur.execute("UPDATE rooms SET characters = '%s' \
                                    where uui = '%s'" %(characters, uui,))

                self.commit()

#############################################################

################ CHECK FOR ROW/CONTENTS IN DB ################

    def in_rooms(self, uui):
        '''check for room existence in database'''
        self.cur.execute('SELECT * from rooms WHERE \
                                   uui="%s"'\
                                   %(uui,))
        result = self.cur.fetchall()
        # print(result)
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

    def in_items(self, name, in_possession):
        '''check for item in database. can be in possession of a room or a
           user'''

        name, in_possession

        self.cur.execute('SELECT * from items WHERE name="%s" AND \
                        in_possession="%s"' %(name, in_possession,))

        result = self.cur.fetchall()
        if(len(result) > 0):
            return True, result
        else:
            return False, ("Error: item [" + str(name) + \
                          "] not in possession of " + str(in_possession))
    
#############################################################

################ LOAD A ROOM OBJECT INTO DB #################

    def load_room(self, room):
        '''load room object into database'''

        uui = room.getUniqueID() 
        name = room.getDisplayName()
        description = room.getDescription()
        exits = self.parse_exits(room.getExits())
        characters = self.parse_characters(room.getCharacters())
        items = self.parse_items(room.getItems())
        
        self.add_room((uui, name, description, \
                           exits, characters, items))

    
    def parse_items(self, items_dict):
        '''parse room object's items into DB compatible format'''

        items_list = []
        for i in items_dict:
            item = i.getName()
            items_list.append("[" + item + "]")
        
        items_string = ""
        for item in items_list:
            items_string += item
        
        return items_string

    def parse_characters(self, characters_dict):
        '''parse room object's characters into DB compatible format'''

        char_list = []
        for c in characters_dict.values():
            char_name = c.get_name()
            char_list.append("[" + char_name + "]")

        characters_string = ""
        for char in char_list:
            characters_string += char
        
        return characters_string

    def parse_exits(self, exits_dict):
        '''parse room object's neighbors into DB compatible format'''
        exits_list = []

        directions = exits_dict.keys()
        directions = list(directions)
        index = 0

        for val in exits_dict.values():
            display_name = val.getDisplayName()
            unique_id = val.getUniqueID()
            exits_list.append("[" + str(unique_id) + ", " + str(display_name) + \
                         ", " + directions[index] + "]")
            index += 1
        
        exits_string = ""
        for exit in exits_list:
            exits_string += exit
        
        return exits_string

#############################################################

############### RETRIEVE A ROOM OBJECT FROM DB ##############

    def retrieve_room(self, data):
        '''main function to facilitate receiving room from DB'''
        boolean, row = self.in_rooms(data)
        if boolean == True:
            uui = row[0][0]
            name = row[0][1]
            description = row[0][2]
            room = Room(uui, name, description)
            
            exits = self.retrieve_exits(row[0][3])
            for exit in exits:
                split = exit.strip("[]").split(",")
                identifiers = str(split[0]) + str(split[1])
                direction = str(split[2])
                room.addNeighbor(identifiers, direction)

            print("print row: " + str(row[0][4]))
            characters = self.retrieve_character(row[0][4])
            
            for character in characters:
                room.addCharacter(character)

            items = self.retrieve_items(row[0][5], uui)
            for item in items:
                room.addItems(item)

            return room
    
    def retrieve_exits(self, room_exits):
        '''retrieves exits from room DB entry and returns them as a list of 
           strings to be parsed as room name/uui and exit direction'''
        res = re.findall(r'\[.*?\]', room_exits.strip(","))
        exits = []

        for item in range(len(res)):
            exit = res[item].strip(",")
            exits.append(exit)
        
        return exits


    def retrieve_character(self, room_characters):
        '''retrieves characters from room DB entry and returns them as a list
           of character objects'''

        res = re.findall(r'\[.*?\]', room_characters.strip(""))

        users = Database("users.db")
        items_db = Database("items.db")

        characters = []
        for char in range(len(res)):
            username = res[char].strip("[]")
            boolean, result = users.in_users(username)
            if (boolean == True):
                name, password, description, \
                location, items, hp = users.retrieve_character_data(result)

                character = Character(name, password, description, location)
                for i in items:
                    in_items, item = items_db.in_items(i, character.get_name())
                    character.addToInventory(item)
                character.updateHP(hp)

                characters.append(character)
        
        return characters


    def retrieve_character_data(self, data):
        '''helper function parses through character data for character object 
           creation'''

        name = data[0][0]
        password = data[0][1]
        description = data[0][2]
        location = data[0][3]
        items = data[0][4].split(", ")
        hp = data[0][5]
        
        return (name, password, description, location, items, hp)

    
    def retrieve_items(self, room_items, uui):
        '''retrieves items from room DB entry and returns them as a list
           of item objects'''

        # print(room_items)
        res = re.findall(r'\[.*?\]', room_items.strip("").strip(""))
        
        items_db = Database("items.db")

        items = []
        for i in range(len(res)):
            item_name = res[i].strip("[]")
            boolean, result = items_db.in_items(item_name, uui)
            if (boolean == True):
                name, description, visible = items_db.retrieve_item_data(result)
                item = Items(name, description, visible, uui)
                items.append(item)
        return items


    def retrieve_item_data(self, data):
        '''helper function parses through item data for item object 
           creation'''
        name = data[0][0]
        description = data[0][1]
        visible = data[0][2]

        return (name, description, visible)
    

    def return_all_rooms(self):
        '''function to return all rooms saved into database'''

        self.cur.execute('SELECT * from rooms')
        db = self.cur.fetchall()

        rooms = []
        for entry in db:
            rooms.append(self.retrieve_room(entry[0]))

        return rooms

#############################################################

    def retrieve_user(self, username):
        in_user, user_data = self.in_users(username)
        if (in_user == True):
            description = user_data[0][2]
            location = user_data[0][3]
            pswd = user_data[0][1]
            inventory = user_data[0][4]
            hp = user_data[0][5]

        character = Character(username, pswd, description, location)

        items = self.retrieve_items(inventory, username)
        for item in items:
            character.addToInventory(item)

        character.updateHP(hp)

        return character


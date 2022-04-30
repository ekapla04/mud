import sys

from src.character import Character
from src.map import Map
from basic_commands import default_cmd_set
from src.room import Room
from db import Database

class GameState:
    def __init__(self, db_location):
        self._db = Database("game.db")
        self._characters = {}  # name -> connection object
        self._Map = None

        self.load_world()

    def connect_character(self, name, password, websocket):
        exists, result = self._db.in_users(name)
        
        char = None

        if exists:
            char = self._db.retrieve_user(name)
            # Put character in the correct location
            loc = self._Map.get_room(char.getLocation().lower().strip())
            char.setLocation(loc)
            loc.addCharacter(char)

            if not char.compare_pswd(password.strip()):
                return "Passwords do not match!" 

        else:
            loc = self._Map.get_room("atrium")
            char =  Character(name, password, "A gentle soul shrouded in mist.", loc)
            self._db.add_user(char)
            loc.addCharacter(char)

        
        # Attatch the message function
        char.set_socket(websocket)

        # Attatch commands
        char.load_command_set(default_cmd_set())

        # Add the character to the list of connected characters
        self._characters[char.get_name()] = char

        return "ok"


    def disconnect_character(self, name):
        if name in self._characters:
            char = self._characters.pop(name)

            # Remove the character from their location
            location = char.getLocation()
            if not location is None:
                location.removeCharacter(char)
                location.broadcast_all(char, f"{char.get_name().capitalize()} has disconnected.")

            # Remove character from their combats if any
            combat = location.getCombat(char)
            if not combat is None:
                combat.disconnect_character(char)

            self._db.change_user_room(char.get_name(), location.getUniqueID())


    def create_character(self, name, password, roomname, websocket):
        exists, toss = self._db.in_users(name)
        print(f"exists {exists}")

        if not exists:
            char = Character(name, password, "A gentle soul shrouded in mist.", self._Map.get_room("atrium"))
            print("add attempt  ", self._db.add_user(char))
            self.connect_character(name, password, websocket)
            return "ok"
        else:
            return "username already in use"


    def load_world(self):
        print("Loading world")
        self._db.create_roomDB()
        self._db.create_userDB()

        # make a temporary map
        self._Map = Map()

        rooms = self._db.return_all_rooms()
        for room in rooms:
            self._Map.addRoom(room)
        
        self._Map.linkExits()



        print("World loaded")


    def message_all(self, msg):
        print(self._characters)
        for char in self._characters.values():
            char.message(msg)


    def get_character(self, char_name):
        return self._characters.get(char_name)


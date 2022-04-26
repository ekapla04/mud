import sys
# sys.path.append("/Users/madeleinestreet/Documents/GitHub/mud/src")

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
        # Create the character object
        char =  Character(name, password, "A gentle soul with blond hair", self._Map.get_room("atrium"))
        
        # Attatch the message function
        char.set_socket(websocket)

        # Attatch commands
        char.load_command_set(default_cmd_set())

        # Add character to room
        self._Map.get_room("atrium").addCharacter(char)

        # Add the character to the list of connected characters
        self._characters[char.get_name()] = char


        return "ok"


    def disconnect_character(self, name):
        if name in self._characters:
            self._characters.pop(name)


    def create_character(self, name, password, roomname, websocket):
        self.connect_character(name, password, websocket)
        return "ok"

    def load_world(self):
        print("Loading world")
        self._db.create_roomDB()
        self._db.create_userDB()

        # make a temporary map
        self._Map = Map()

        self._Map.roomFromNameID("Atrium", "atrium", """A two story tall atrium with grand windows, \
            a central fountain and an excess of green leafy plants.""")
        self._Map.roomFromNameID("Main Hall", "mainhall", """A large, extravagant entry hall.\
            The walls are mirrored and at the far end is a large sliding glass door.""")
        self._Map.roomFromNameID("Sitting Room", "sittingroom", """A lush sitting room with \
        luminescent green couches. An intricte portrait of a young woman hangs above the mantle. """)

        atrium = self._Map.get_room("atrium")
        mainhall = self._Map.get_room("mainhall")
        sittingroom = self._Map.get_room("sittingroom")

        atrium.addNeighbor(mainhall, "south")
        mainhall.addNeighbor(atrium, "north")
        atrium.addNeighbor(sittingroom, "east")
        sittingroom.addNeighbor(atrium, "west")   


        print("World loaded")


    def message_all(self, msg):
        print(self._characters)
        for char in self._characters.values():
            char.message(msg)

    def get_character(self, char_name):
        return self._characters.get(char_name)


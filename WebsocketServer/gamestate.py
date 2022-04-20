import sys
sys.path.append("/Users/madeleinestreet/Documents/GitHub/mud/src")

from character import Character
from map import Map
from basic_commands import default_cmd_set


class GameState:
    def __init__(self, db_location):
        self._db = None
        self._characters = {}  # name -> character object
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
        self._Map = Map()
        self._Map.roomFromNameID("Atrium", "atrium", "A high ceilinged room filled with plants.")

    def message_all(self, msg):
        print(self._characters)
        for char in self._characters.values():
            char.message(msg)

    def get_character(self, char_name):
        return self._characters.get(char_name)


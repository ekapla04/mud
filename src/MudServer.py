import selectors
import socket
import socketserver
import threading

from MudClientHandler import MudClientHandler
from character import Character
from map import Map
from basic_commands import default_cmd_set

HOST, PORT = "localhost", 8000


class MudServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __init__(self, server_address: tuple[str, int], RequestHandlerClass,
                 bind_and_activate: bool = ..., ):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.db = None
        self._Map = Map()
        self._characters = {}

        self._Map.roomFromNameID("Atrium", "atrium", "A high ceilinged room filled with plants.")

    def character_connected(self, character):
        print("A new character connected: ", character)

        # For testing: message all
        # for c in self._characters.values():
        #     c.message(character.get_name() + " has joined!")

    def character_disconnected(self, character):
        self._characters.pop(character.get_name())

    def login_character(self, name, password, roomname=None):
        """
            login_character - checks the database for a character with the
                matching name and password

            returns - the character object if it exists and None otherwise
        """
        # TODO: Implement the db check so the character object is returned
        char =  Character(name, password, "A gentle soul with blond hair", self._Map.get_room("atrium"))

        # Load commands
        char.load_command_set(default_cmd_set())

        # add character to room
        self._Map.get_room("atrium").addCharacter(char)

        self._characters[char.get_name()] = char
        return char

    def create_new_character(self, name, password, desc, roomname):
        """
            create_new_character - Called when a new character is created

            name: string, name of the character
            password: string, verified password
            desc: string, the desired description of the character
            roomname: string, name of the room to place them in
        """
        # TODO: Add the new character to the database and log them in

        char = Character(name, password, desc, self._Map.get_room("atrium"))

        self._Map.get_room("atrium").addCharacter(char)

        char.load_command_set(default_cmd_set())

        self._characters[char.get_name()] = char

        return char


server = MudServer((HOST, PORT), MudClientHandler)

# Run the server in a thread
# This should allow us to stop it when we want to, and do some other things after
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

print("Server Started")

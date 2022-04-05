import selectors
import socket
import socketserver
import threading
from MudClientHandler import MudClientHandler


HOST, PORT = "localhost", 8000


class MudServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __init__(self, server_address: tuple[str, int], RequestHandlerClass,
                 bind_and_activate: bool = ..., ):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.db = None
        self._Map = None
        self._characters = {}

    def character_connected(self, character):
        print("A new character connected: ", character)

    def character_disconnected(self, character):
        pass

    def login_character(self, name, password, room=None):
        """
            login_character - checks the database for a character with the
                matching name and password

            returns - the character object if it exists and None otherwise
        """
        # TODO: Implement the db check so the character object is returned
        return "not yet implemented"

    def create_new_character(self, character):
        """
            create_new_character - Called when a new character is created

            character - the newly created character object
        """
        # TODO: Add the new character to the database and log them in
        pass


server = MudServer((HOST, PORT), MudClientHandler)

# Run the server in a thread
# This should allow us to stop it when we want to, and do some other things after
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

print("Server Started")

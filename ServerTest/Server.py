import selectors
import socketserver
import threading
import time
import select

HOST, PORT = "localhost", 8000


class MudClientHandler(socketserver.StreamRequestHandler):
    """
        Override of default handler class that defines what to do with each
        client connection
    """
    def handle(self):
        print("Hello from: ", self.client_address)

        # Load character

        # Enter main game loop
        sel = selectors.DefaultSelector()
        sel.register(self.connection, selectors.EVENT_READ, None)

        while True:
            # Get a message
            events = sel.select()
            for key, mask in events:
                if mask == selectors.EVENT_READ:
                    message = self.rfile.readline().decode().strip()
                    if message != " ":
                        self.server.parse(message, self.connection)

            # Check that client is still connected
            self.send_message(" ")


    def send_message(self, message):
        HEADER_LENGTH = 16
        message = message.encode("utf-8")
        self.wfile.write(f"{len(message):<{HEADER_LENGTH}}".encode("utf-8"))
        self.wfile.write(message)


class MudServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
        The main server class which starts a new thread to deal with
        each incoming connection
    """
    def __init__(self, address):
        super().__init__(address, MudClientHandler)
        self._characters = {}

    def parse(self, message, connection):
        print(message)
        self.send_message(message.upper(), connection)

    @staticmethod
    def send_message(message, connection):
        HEADER_LENGTH = 16
        message = message.encode("utf-8")
        connection.sendall(f"{len(message):<{HEADER_LENGTH}}".encode("utf-8"))
        connection.sendall(message)

server = MudServer((HOST, PORT))

# Run the server in a thread
# This should allow us to stop it when we want to, and do some other things after
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

print("Server Started")

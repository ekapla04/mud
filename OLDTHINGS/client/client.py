import selectors
import socket
import sys
import threading


class Client:
    def __init__(self):
        self._HOST, self._PORT = (None, None)
        self._HEADER_LENGTH = 16
        self._sock = None
        self.isDead = False
        self.isQuit = False

        # self._mailbox = queue.Queue()
        # self._outbox = queue.Queue()

    def start(self, address):
        """
            start - runs a connection to a server until the user quits
                    or the connection is lost

            address: (Host, Port)
        """
        # Create a connection to the provided address
        self._HOST, self._PORT = address
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with self._sock as sock:
            # Connect to the server
            try:
                sock.connect((self._HOST, self._PORT))
            except ConnectionRefusedError:
                print("Connection failed")
                return

            # A note about starting the threads: if you start these in the
            # reverse order (input and then receive), receive can never print.
            # I'm not sure what the deal with that is, so when we plug this
            # into the GUI we'll have to make sure that the get_input and
            # handle_message functions don't conflict in a weird way

            # Start a thread to get messages from server
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()

            # Start a thread to get commands from user
            input_thread = threading.Thread(target=self.collect_input())
            input_thread.start()

            receive_thread.join()
            input_thread.join()

    def receive_messages(self):
        """
            receive_messages - the message receiving loop, waits for messages
                               from the server and dispatches them to be
                               dealt with
        """
        # Selector used to tell if there are things to read from the server
        sel = selectors.DefaultSelector()
        sel.register(self._sock, selectors.EVENT_READ, None)

        while not self.isDead and not self.isQuit:
            # Events is a list of objects that are ready for either reads,
            # writes, or errors. In our case it will always be read events
            # because that's the only thing registered to this selector
            events = sel.select()

            for key, mask in events:
                if mask == selectors.EVENT_READ:
                    message = self.get_message()

                    # If the message is None, the server is disconnected
                    if message is None:
                        print("Server Disconnected")
                        self.close()
                        break

                    # Handle the incoming message
                    self.handle_message(message)


    def collect_input(self):
        """
            collect_input - the input collecting loop, collects input and
                            sends it to the server
        """
        while not self.isDead and not self.isQuit:
            message = self.get_input().strip()

            if message == "":          # Never send empty messages to the server
                continue

            # Attempt to send the message to the server
            # If it doesn't work, the connection is closed
            if not self.send_message(message):
                print("Server disconnected")
                self.close()

    def handle_message(self, msg):
        """
            handle_message - deal with an incoming server message
                             TODO: overwrite when plugged into the GUI
        """
        print(msg)

    def get_input(self):
        """
            get_input - gets an input from the user,
                        TODO: overwrite when GUI is plugged in

            returns: the message collected
        """
        return input("> ")

    def server_living(self):
        """
            server_living - returns True if the connection is still alive
                            and False otherwise
        """
        # Receive a dummy message, if it is "" then the server is closed
        # Set the flags MSG_PEEK and MSG_DONTWAIT so that the message is not
        # removed from the socket and the call doesn't wait for a message
        msg = self._sock.recv(10, socket.MSG_PEEK | socket.MSG_DONTWAIT)
        if msg.decode() == "":
            return False
        return True

    def get_message(self):
        """
            get_message - receives and returns a message from the server

            returns - the decoded method received from the server, or None
                      if the server is disconnected
        """
        # Get the message header, says how long the expected message is
        header = self._sock.recv(self._HEADER_LENGTH)

        # If the header is the empty string, the server is closed
        if header.strip() == b'':
            return None
        else:
            # Receive a message of the correct length
            header = int(header.decode("utf-8").strip())
            message = self._sock.recv(header).decode()

            if message == "":
                return None
            return message

    def send_message(self, msg):
        """
            send_message - sends a message to the server

            returns - returns True if the message sent without error and
                      False otherwise (usually bc of server disconnect)
        """
        # Never send an empty message to the server!
        if msg.strip() == "":
            return True

        try:
            length = self._HEADER_LENGTH
            msg = msg.encode("utf-8")

            # Packs the message into a message of length length
            self._sock.sendall(f"{len(msg):<{length}}".encode("utf-8"))

            self._sock.sendall(msg)
            return True
        except:
            return False

    def close(self):
        """
            close - shuts down the socket and tells threads to kill themselves
        """
        self._sock.close()
        self.isDead = True
        self.isQuit = True



def main(argv):
    host, port = ("localhost", 8000)
    # The client can either use the default connection info
    # or provide their own.
    if len(argv) == 1:
        pass
    elif len(argv) == 3:
        host, port = (argv[1], int(argv[2].strip()))
    else:
        print("USAGE: python3 Client.py [hostname port]")
        exit(1)

    client = Client()

    client.start((host, port))


if __name__ == "__main__":
    main(sys.argv)

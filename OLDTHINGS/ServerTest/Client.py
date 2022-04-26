import selectors
import socket
import sys
import queue
import threading


class Client:
    def __init__(self):
        self._HOST, self._PORT = (None, None)
        self._HEADER_LENGTH = 16
        self._sock = None
        self.isDead = False

        self._mailbox = queue.Queue()
        self._outbox = queue.Queue()


    def start(self, address):
        self._HOST, self._PORT = address
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with self._sock as sock:
            # Connect to the server
            try:
                sock.connect((self._HOST, self._PORT))
            except ConnectionRefusedError:
                print("Connection failed")
                return

            # Start a thread to get commands from user
            input_thread = threading.Thread(target=self.send_commands)
            input_thread.start()

            # Start a thread to get messages from server
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()

            input_thread.join()
            receive_thread.join()

    def get_message(self):
        """
            Called when there is a read event in the file
            TODO: currently just prints out the message, maybe make better?
                Possibly by putting it in _mailbox and producer consumering?
        """
        header = self._sock.recv(self._HEADER_LENGTH)

        if header.strip() == b'':
            return None
        else:
            header = int(header.decode("utf-8").strip())
            message = self._sock.recv(header).decode()
            return message

    def receive_messages(self):
        """
            Receive messages in a loop
            TODO: Add better documentation
        """
        sel = selectors.DefaultSelector()
        sel.register(self._sock, selectors.EVENT_READ, None)

        while not self.isDead:
            events = sel.select()
            for key, mask in events:
                if mask == selectors.EVENT_READ:
                    message = self.get_message()
                    if message is None:
                        print("Server Disconnected")
                        self.close()
                        break
                    if message != " ":
                        print(message)

    def send_commands(self):
        """
            send_commands takes a socket with an open connection and sends
            user input messages in a loop
        """
        message = ""
        while not self.isDead:
            message = input("> ").strip()

            if message == "":          # Never send empty messages to the server
                continue

            # Attempt to send the message to the server
            # As of this moment, no header is included
            try:
                self._sock.sendall((message + "\n").encode("utf8"))
            except:     # TODO: figure out which exceptions might be thrown
                print("Server disconnected")
                self.close()
                break

    def close(self):
        self.isDead = True
        self._sock.close()


    # def receive_reply(self):
    #     """
    #         Takes in a socket with an open connection and takes in replies, then
    #         adds them to a queue of responses
    #     """
    #     while True:
    #         header = self._sock.recv(self._HEADER_LENGTH)
    #         header = int(header.decode("utf-8").strip())
    #         message = self._sock.recv(header).decode()
    #         print(message)
    #         if message == "quit":
    #             break

    #
    # def send_cb(self):
    #     if not self._outbox.empty():
    #         message = self._outbox.get().strip()
    #         if message == "":
    #             return
    #
    #         try:
    #             self._sock.sendall((message + "\n").encode("utf8"))
    #             # print("---sent---")
    #         except:     # TODO: figure out which exceptions might be thrown
    #             print("Server disconnected")
    # def collect_commands(self):
    #     """
    #         Gets commands from the user in a loop until quit is typed
    #         adds them to the outbox
    #     """
    #     command = ""
    #     while command != "quit":
    #         command = input("> ").strip()
    #         if command == "":
    #             continue
    #
    #         self._outbox.put(command)

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
import selectors
import socket
import socketserver
import threading
from character import Character


class ClientDead(Exception):
        """ Raised when the client is found dead """
        pass


class MudClientHandler(socketserver.StreamRequestHandler):
    HEADER_LENGTH = 16

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self._character = None

    # OK I HAVE NO IDEA WHAT THE DEAL IS, BUT IF SET UP IS OVERRIDDEN NOTHING WORKs....
    # def setup(self):
    #     # self.__character = None
    #     pass

    def handle(self):
        """
            handle - does all the work of handling a connection
        """
        print("Hello from: ", self.client_address)

        isDead = False
        isQuit = False

        # TODO: Add a welcome to the game ascii art message!!!

        # The first message the server is expecting is the login/character
        # creation string of the form:
        #       login // name // password
        #       create // name // password // room

        self._character = None

        try:
            resultdesc, character = "", None
            while resultdesc != "ok":
                self.send_msg("Enter login string (mode of loging // name // password [// roomname])")

                startstr = self.get_one_response()
                resultdesc, character = self.load_character(startstr)
                if resultdesc != "ok":
                    self.send_msg(f"Error loading character: {resultdesc}")
            self.send_msg(f"Connected as {character.get_name()}")

            self._character = character

            self._character.message = self.send_msg

        except ClientDead:
            print("Client is dead, that's what went wrong")
            return
        except Exception as e:
            print("Failure to load character: ", str(e))
            return


        # ======== MAIN GAME LOOP ==========
        try:
            sel = selectors.DefaultSelector()
            sel.register(self.connection, selectors.EVENT_READ, None)

            while not isDead and not isQuit:
                events = sel.select()
                for key, mask in events:
                    if mask == selectors.EVENT_READ:
                        message = self.receive_message()

                        command, args = self.parse_command(message)
                        self.execute_command(command, args)
        except ClientDead:
            print("ClientDead raised by connection at: ", self.client_address)
            return

        print("Goodbye from: ", self.client_address)

    def finish(self):
        """
            finish - called when handle returns, removes the current character
                     from the server
        """
        print("Client at ", self.client_address, " disconnected.")
        if not self._character is None:
            self.server.character_disconnected(self._character)

    # ============ HELPER METHODS ============

    def is_living(self):
        """
                    is_living - returns True if the connection is still alive
                                and False otherwise
        """
        msg = self.connection.recv(10, socket.MSG_PEEK | socket.MSG_DONTWAIT)
        if msg.decode() == "":
            return False
        return True

    def send_msg(self, msg):
        """
            send_msg - sends a message to the client

            returns - True if the message send was succesful

            raises - ClientDead if the connection is closed
        """
        try:
            header_length = self.HEADER_LENGTH
            msgb = msg.encode("utf-8")
            self.connection.sendall(f"{len(msgb):<{header_length}}".encode("utf-8"))
            self.connection.sendall(msgb)
            return True
        except:
            # Do clean up, handle should know to exit
            raise ClientDead

    def receive_message(self):
        """
            get_message - receives and returns a message from the client

            returns - the decoded method received from the server

            raises: ClientDead if the client is disconected
        """

        try:
            # Get the message header, says how long the expected message is
            header = self.connection.recv(self.HEADER_LENGTH)

            # If the header is the empty string, the server is closed
            if header.strip() == b'':
                raise ClientDead
            else:
                # Receive a message of the correct length
                header = int(header.decode("utf-8").strip())
                message = self.connection.recv(header).decode()

                if message == "":
                    raise ClientDead
                return message

        except ConnectionResetError:
            raise ClientDead

    def get_response_from(self, options, prompt=None, case_sensitive=False, ):
        """
            get_response_from - prompts the user for an answer from a list
                of responses

            options - a dictionary of the form
                    ["response title": {set of options}]
                    ex: ["yes" : {"yes", "y"}, "no" : {"no", "n"}]

            prompt - Message to send when a wrong answer is given

            returns - The key associated with the given response or None if
                      the client disconnects

            TODO: Add a way of asking what options are available
        """
        # If the search is not case sensitive, make all options lowercase
        if not case_sensitive:
            for key in options.keys():
                new = {None}
                for item in options[key]:
                    new.add(item.lower())
                new.remove(None)
                options[key] = new

        sel = selectors.DefaultSelector()
        sel.register(self.connection, selectors.EVENT_READ, None)

        result = None

        # Prompt the user for a response until they provide a valid answer
        while result is None:
            # For each read event, check to see if the response is in the 
            # list of allowed responses
            events = sel.select()
            for key, mask in events:
                if mask == selectors.EVENT_READ:

                    msg = self.receive_message()
                    msg = msg.strip()

                    if not case_sensitive:
                        msg = msg.lower()

                    # Check if the message corresponds to an allowable option
                    for key in options.keys():
                        if msg in options[key]:
                            result = key

                    # If result was not set then the response was not allowed
                    # and we prompt the user to try again.
                    if result is None:
                        self.send_msg(prompt)

        return result

    def yes_or_no(self, prompt="Enter yes/no"):
        """
            yes_or_no - prompts the user to respond with either yes or no

            returns - "yes" or "no" or None if the client disconnects
        """
        options = {"yes": {"yes", "y"}, "no": {"no", "n"}}
        return self.get_response_from(options, prompt)

    def get_one_response(self):
        """
            Waits for one response from the user and returns the message or
            None if the client is disconnected
        """
        sel = selectors.DefaultSelector()
        sel.register(self.connection, selectors.EVENT_READ, None)

        while True:
            events = sel.select()
            for key, mask in events:
                if mask == selectors.EVENT_READ:
                    msg = self.receive_message()

                    return msg.strip()

    # ============ SPECIAL INTERACTIONS ==============

    def parse_command(self, text):
        """
            parse_command - breaks the command into command word and arguments
            text - non-empty, non-whitespace string representing the user's input
            returns - a tuple of the form ("command", ["list", "of", "args"])
        """
        text = text.strip().split()
        command = text[0]
        text.pop(0)
        return (command, text)

    def execute_command(self, command, args):
        """
            execute_command - excecutes the given command
            TODO - Make it do the thing!
        """
        print(command, args)

        found = False
        cmd_set = self._character.get_commands()
        for cmd in cmd_set.values():
            if cmd.is_this_command(command):
                found = True
                cmd.execute(self._character, args, self.server)

        if not found:
            print("command not found, try movement")
            # update found if movement is possible

        if not found:
            print("no exits, unknown command!")


        # self.send_msg(f"command: {command} with args: {args}")

    def load_character(self, startstr):
        """
            Loads the user's desired character based on the login string

            Returns a tuple of the form ("result description", character object)
                On a success it will be of the form ("ok", character)
                On a failure it will be of the form ("error message", None)
            -------
            startstr: string of the form
                "login // name // password" or
                "create // name // password // room"
        """
        items = startstr.split("//")

        if len(items) < 3:
            return ("Not enough elements in string", None)

        # User wants to login as an existing character
        if items[0].strip().lower() == "login":
            char = self.server.login_character(items[1].strip().lower(), items[2].strip())
            if char is None:
                return ("Bad character info", None)
            else:
                return("ok", char)

        # User wants to create a character
        elif items[0].strip().lower() == "create":
            if len(items) != 4:
                return ("Wrong number of elements in string", None)

            password = items[2].strip()
            if password != password:  # TODO: validate password correctly!
                return("Invalid password", None)

            char = self.server.create_new_character(items[1].strip().lower(), password,
                                                    "a glowing description", items[3].strip().lower())
            return ("ok", char)

        else:
            return ("Bad first element", None)

        return ("not yet implemented", None)

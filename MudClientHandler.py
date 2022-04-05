import selectors
import socket
import socketserver
import threading


# I fucked up and should be using an exception for when the client disconnects
# instead I beefed it and have to check for None EVERY TIME, I might try to
# fix it but idk how long that would take...

class MudClientHandler(socketserver.StreamRequestHandler):
    HEADER_LENGTH = 16

    # def __init__(self, request, client_address, server):
    #     super().__init__(request, client_address, server)

    def handle(self):
        """
            handle - does all the work of handling a connection
        """
        print("Hello from: ", self.client_address)

        isDead = False
        isQuit = False

        # TODO: Add a welcome to the game ascii art message!!!

        character = None

        self.send_msg("Would you like to create a new character?")
        resp = self.yes_or_no()
        if resp is None:
            return
        elif resp == "yes":
            character = self.character_creation()
        else:
            character = self.login()

        if character is None:  # The client disconnected...
            return

        self.send_msg("Logged in as: " + character)

        # ======== MAIN GAME LOOP ==========

        sel = selectors.DefaultSelector()
        sel.register(self.connection, selectors.EVENT_READ, None)

        while not isDead and not isQuit:
            events = sel.select()
            for key, mask in events:
                if mask == selectors.EVENT_READ:
                    message = self.receive_message()

                    if message is None:
                        isDead = True
                        return

                    command, args = self.parse_command(message)
                    self.execute_command(command, args)

        print("Goodbye from: ", self.client_address)

    def finish(self):
        """
            finish - called when handle returns, removes the current character
                     from the server
        """
        print("Client at ", self.client_address, " disconnected.")
        self.server.character_disconnected("character")

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

            returns - True if the message send was succesful, and False if the
                      connection is closed
        """
        try:
            header_length = self.HEADER_LENGTH
            msgb = msg.encode("utf-8")
            self.connection.sendall(f"{len(msgb):<{header_length}}".encode("utf-8"))
            self.connection.sendall(msgb)
            return True
        except:
            # Do clean up, handle should know to exit
            return False

    def receive_message(self):
        """
            get_message - receives and returns a message from the client

            returns - the decoded method received from the server, or None
                       if the server is disconnected
        """

        try:
            # Get the message header, says how long the expected message is
            header = self.connection.recv(self.HEADER_LENGTH)

            # If the header is the empty string, the server is closed
            if header.strip() == b'':
                return None
            else:
                # Receive a message of the correct length
                header = int(header.decode("utf-8").strip())
                message = self.connection.recv(header).decode()

                if message == "":
                    return None
                return message

        except ConnectionResetError:
            print("Error with ", self.client_address, " disconnected")
            return None

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

        while result is None:
            events = sel.select()
            for key, mask in events:
                if mask == selectors.EVENT_READ:
                    msg = self.receive_message()

                    # If message received is None, the client is disconnected
                    if msg is None:
                        return None

                    msg = msg.strip()

                    if not case_sensitive:
                        msg = msg.lower()

                    for key in options.keys():
                        if msg in options[key]:
                            result = key

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

                    if msg is None:
                        return None

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
        self.send_msg(f"command: {command} with args: {args}")

    def character_creation(self):
        """
            character_creation - leads the user through character creation

            returns - The new character object, or None if the client
                      disconnects
        """

        # Pick a character name
        # TODO: Decide on the guidelines for character names
        self.send_msg("""Pick a character name""")
        name = None
        while name is None:
            msg = self.get_one_response()
            if msg == None:
                return None

            # TODO: validate name
            name = msg.strip().lower()

        # Pick + verify password
        password = None
        while password is None:
            self.send_msg("""Pick a password""")
            msg = self.get_one_response()
            if msg is None:
                return None

            # TODO: Validate password
            password = msg

            self.send_msg("Verify password")

            msg = self.get_one_response()
            if msg is None:
                return None

            if password != msg:
                self.send_msg("Passwords do not match")
                password = None

        # Other character creation things like skills, and appearance

        # Pick a starting room
        starting_options = {"atrium": {"1", "atrium"},
                            "powder room": {"2", "powder room", "powder"}}
        self.send_msg("""Pick a starting room from the following list:
            1 - Atrium
            2 - Powder Room""")
        room_choice = self.get_response_from(starting_options, "Pick atrium(1) or powder room(2)")

        # TODO: Create a new character object with the collected info

        self.server.create_new_character("Character")

        return "character"

    def login(self):
        """
            login - get the user's character name and password and log them
                    into the game

            return - The user's character object

            TODO: Add a way switch to character creation? (or not)
        """
        character = None

        while character is None:
            self.send_msg("Enter character name")
            char_name = self.get_one_response()

            self.send_msg("Enter password")
            password = self.get_one_response()

            character = self.server.login_character(char_name, password)

            if character is None:
                self.send_msg("Login attempt failed. Character name or password are incorrect.")

        return character
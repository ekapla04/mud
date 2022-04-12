'''
    Class representing character object
'''
from threading import Lock
from command import Command

class Character:
    def __init__(self, name, pswd, descr, room):
        self.__name = name
        self.__description = descr
        self.__location = room
        self.__pswd = pswd
        self.__inventory = []
        self.__hp = 100
        self.__commands = {}
        self.__hpMutex = Lock()
        self.message = self.__message_not_set
    
    def getLocation(self):
        return self.__location

    def addToInventory(self, item):
        '''
            Method to add to inventory
            Parameters:
            ------------
            item: items object
        '''
        self.__inventory.append(item)

    def getInventory(self):
        return self.__inventory

    def updateHP(self, score):
        '''
            Method to update HP of character

            Parameters:
            ------------
            score: int
        '''
        with self.__hpMutex:
            self.__hp += score

    def getHP(self):
        '''
            Method to retrieve HP of character

            Return
            ------------
            res: int
        '''
        with self.__hpMutex:
            res = self.__hp
        
        return res

    def __message_not_set(self, msg):
        """
            __message_not_set - placeholder method for when the message function
                is not yet set

            ---------
            msg : string
        """
        print("Message function not set, unable to send [", msg, "] to ", self.__name)

    def get_name(self):
        return self.__name

    def get_desc(self):
        return self.__description


    # None of these are protected with a mutex under the assumption that
    # After the character is initialized, we don't change them
    # If that changes we should move where some of this logic lives
    def load_command_set(self, commands):
        """
            Replaces the old command set with a new one
        """
        self.__commands = commands

    def add_command(self, command: Command):
        """
            Add a new command to the command set
        """
        self.__commands[command.get_name()] = command

    def get_commands(self):
        return self.__commands

    def message_location(self, msg):
        """
            Message all users in the current room except yourself
        """
        self.__location.broadcast(self, msg)
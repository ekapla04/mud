'''
    Class representing character object
'''

import sys
sys.path.append("pypackages")

from threading import Lock
from src.command import Command
import websockets
import json
import asyncio

class Character:
    def __init__(self, name, pswd, descr, room):
        self.__name = name
        self.__description = descr
        self.__location = room
        self.__pswd = pswd
        self.__inventory = []
        self.__hp = 3
        self.__commands = {}
        self.__hpMutex = Lock()        
        self.__locationLock = Lock()
        self.__is_fighting = False

        # Related to connection
        self.websocket = None
        self.doing_commands = True
        self.message_queue = asyncio.Queue()
    
    def getLocation(self):
        return self.__location
    def setLocation(self, room):
        self.__location = room

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

    def decrementHP(self):
        with self.__hpMutex:
            if not self.__hp == 0:
                self.__hp = self.__hp - 1

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

    def get_pswd(self):
        return self.__pswd

    def compare_pswd(self, pswd):
        return self.__pswd == pswd

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

    def message_location(self, msg, code="msg"):
        """
            Message all users in the current room except yourself
        """
        self.__location.broadcast(self, msg, code)

    def message(self, msg, code="msg"):
        """
            Message the user
        """
        if not self.websocket is None:
            websockets.broadcast({self.websocket}, json.dumps({"type":code, "text":msg}))
        else:
            print("Websocket not set :(")

    def set_socket(self, web_socket):
        self.websocket = web_socket

    def is_fighting(self):
        """
            Return True if the character is in combat and False otherwise
        """
        result = False
        with self.__hpMutex:
            # result = self.__location.is_fighting(self)
            result = self.__is_fighting
        return result

    def set_is_fighting(self, bool):
        with self.__hpMutex:
            self.__is_fighting = bool
'''
    Class representing room object
'''
from threading import Lock
from combat import Combat

from character import Character

class Room():

    def __init__(self, id, name, description):
        self.__id = id
        self.__displayName = name
        self.__description = description
        self.__exits = {}       # dict of exit names to room objects
        self.__characters = {}  #dic of character names to characters
        self.__items = []       #is it a list of dic
        self.__combats = {}     # dict of combats objects to [fighters]

        self.__charLock = Lock()
        self.__combatsLock = Lock()
        self.__itemLock = Lock()

    def addCharacter(self, character):
        '''
            Method to add characters to a room

            Parameters:
            ----------
            character: character object
            

            Return:
            -------
            status: string (message whether system succeeded or failed)
        '''
        try:
            self.__charLock.acquire()
            self.__characters[character.get_name()] = character
            status = "success"
        except:
            status = "Error"
        finally:
            self.__charLock.release()

        return status

    def removeCharacter(self, character):
        """
            Removes a character from the room
            
            Parameters:
            -------
            character - the character object to remove

            Return:
            -------
            status: string (message whether system succeeded or failed)
        """
        try:
            self.__charLock.acquire()
            if character.get_name() in self.__characters:
                self.__characters.pop(character.get_name())
            status = "success"
        except:
            status = "Error"
        else:
            self.__charLock.release()

    # def challenge(self, challenger, challenged):
    #     '''
    #         Method to manage combat challenges

    #         Parameters:
    #         ----------
    #         challenger: character object who initial challenge
    #         challenged: character object being challenged

    #         Return:
    #         -------
    #         status: string (message whether system succeeded or failed)
    #     '''
    #     try:
    #         self.__charLock.acquire()
    #         combatStatus = self.__characters(challenged)
    #         challengedLocation = challenged.getLocation()

    #         if challengedLocation == self.__id:
    #             if not combatStatus:            #check whether challenged is not in other combat
    #                 combatRoom = Combat(challenger, challenged) # create combat room
    #                 with self.__combatsLock:    # require lock for combat rooms
    #                     self.__combats.append(combatRoom) # add room to combats room

    #                 combatRoom.start()          # initiate the fight
    #                 status = "success"
    #             else:
    #                 status = "Error: challenged denied"
    #         else:
    #             status = "Error: cannot challenger user in a different room"
    #     except:
    #         status = "Error"
    #     finally:
    #         self.__charLock.release()

    #     return status

    def addCombat(self, combat):
        with self.__combatsLock:
            self.__combats[combat] = combat.list_fighters()

    def removeCombat(self, combat):
        with self.__combatsLock:
            self.__combats.delete(combat)

    def broadcast(self, sender, message, code="msg"):
        '''
            Method to broadcast message to all users in the room except the sender

            Parameters:
            ------------
            sender: character object
            message: string (message to broadcast)
        '''
        with self.__charLock:
            for char in self.__characters.values():
                if char.get_name() != sender.get_name():
                    char.message(message, code)

    def broadcast_all(self, sender, message, code="msg"):
        '''
                    Method to broadcast message to all users in the room

                    Parameters:
                    ------------
                    sender: character object
                    message: string (message to broadcast)
                '''
        with self.__charLock:
            for char in self.__characters.values():
                char.message(message, code)
    
    def addNeighbor(self, neighbor, exitname):
        '''
            Method to add neighbors of the room

            Parameters:
            ----------
            neighbor: room object
            exitname: string(North, South, West, East)
            

            Return:
            -------
            status: string (message whether system succeeded or failed)
        '''
        try:
            self.__exits[exitname] = neighbor
            status = "success"
        except:
            status = "Error: cannot add exit to room " + self.__displayName

        return status
    
    def addItems(self, item):
        '''
            Method to add items to the room

            Parameters:
            ----------
            item: items object
            

            Return:
            -------
            status: string (message whether system succeeded or failed)
        '''
        try:
            self.__itemLock.acquire()
            self.__items.append(item)
            status = "success"
        except:
            status = "Error: cannot add item to room " + self.__displayName
        finally:
            self.__itemLock.release()

        return status

    def getUniqueID(self):
        return self.__id

    def getDisplayName(self):
        return self.__displayName

    def getDescription(self):
        return self.__description

    def getExits(self):
        return self.__exits
    def setAllExits(self, exits):
        self.__exits = exits
    
    def getCharacters(self):
        return self.__characters

    def getCombat(self, character):
        result = None
        with self.__combatsLock:
            for combat, fighters in self.__combats.items():
                if character in fighters:
                    result = combat
                    break
        return result

    def is_fighting(self, character):
        """
            Returns True if character is fighting and False otherwise

            ------
            character - character object
        """
        result = False

        # Check if the given character is fighting
        with self.__combatsLock:
            for combat in self.__combats.keys():
                print(combat)
                result = result or combat.is_in(character)
        return result
            
    def isPresent(self, char_name):
        """
            Checks if the named character is present
        """
        result = False
        with self.__charLock:
            result = char_name in self.__characters
        return result

    def getItems(self):
        return self.__items

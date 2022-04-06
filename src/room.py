'''
    Class representing room object
'''
from threading import Lock
from combat import Combat



class Room:
    def __init__(self, id, name, description):
        self.__id = id
        self.__displayName = name
        self.__description = description
        self.__exits = {}
        self.__characters = {}  #dic of chars as keys and combat as val
        self.__items = []       #is it a list of dic
        self.__combats = []
        self.__charLock = Lock()
        self.__combatsLock = Lock()

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
            self.__characters[character] = False
            status = "success"
        except:
            status = "Error"
        finally:
            self.__charLock.release()

        return status

    def challenge(self, challenger, challenged):
        '''
            Method to manage combat challenges

            Parameters:
            ----------
            challenger: character object who initial challenge
            challenged: character object being challenged

            Return:
            -------
            status: string (message whether system succeeded or failed)
        '''
        try:
            self.__charLock.acquire()
            combatStatus = self.__characters(challenged)
            challengedLocation = challenged.getLocation()

            if challengedLocation == self.__id:
                if not combatStatus:            #check whether challenged is not in other combat
                    combatRoom = Combat(challenger, challenged) # create combat room
                    with self.__combatsLock:    # require lock for combat rooms
                        self.__combats.append(combatRoom) # add room to combats room

                    combatRoom.start()          # initiate the fight
                    status = "success"
                else:
                    status = "Error: challenged denied"
            else:
                status = "Error: cannot challenger user in a different room"
        except:
            status = "Error"
        finally:
            self.__charLock.release()

        return status

    def broadcast(self, sender, message):
        '''
            Method to broadcast message to all users in the room

            Parameters:
            ------------
            sender: character object
            message: string (message to broadcast)
        '''
        pass
    
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
            self.__items.append(item)
            status = "success"
        except:
            status = "Error: cannot add item to room " + self.__displayName

        return status
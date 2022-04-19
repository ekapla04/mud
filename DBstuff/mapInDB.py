'''
    Class representing map object

'''
from threading import Lock
import uuid
from roomInDB import Room

class Map:
    def __init__(self):
        self.__rooms = {}
        self.__mutex = Lock()

    def createRoom(self, name, desc):
        roomId = uuid.uuid1()

        if roomId not in self.__rooms.keys():
            newRoom = Room(roomId, name=name, description=desc)
        else:
            return "Error: Cannot duplicate rooms"
            
        with self.__mutex:
            self.__rooms[roomId] = newRoom

        return "Success"

    '''
        Need to discuss all other methods needed for map
    '''

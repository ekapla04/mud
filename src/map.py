'''
    Class representing map object

'''
from threading import Lock
import uuid
from src.room import Room

class Map:
    def __init__(self):
        self.__rooms = {}  # maps room id to room
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

    def roomFromNameID(self, name, room_id, desc):
        """
            Add a new room with a given room id (string)
        """
        if room_id not in self.__rooms.keys():
            newRoom = Room(room_id, name=name, description=desc)
        else:
            return "Error: Cannot duplicate rooms"

        with self.__mutex:
            self.__rooms[room_id] = newRoom

        return "Success"

    '''
        Need to discuss all other methods needed for map
    '''
    def get_room(self, roomname):
        """
            Return the room with the name roomname from the map
        """
        room = None
        with self.__mutex:
            if roomname in self.__rooms:
                room = self.__rooms[roomname]
        return room

    def place_character(self, character, roomid):
        """
            place_character - adds a character to the named room

            character - character object to add
            roomid  - string, name of room
        """
        pass

    def remove_character(self, character, roomid):
        """
            remove_character - adds a character to the named room

            character - character object to remove
            roomid  - string, name of room
        """
        pass

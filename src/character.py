'''
    Class representing character object
'''
from threading import Lock

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




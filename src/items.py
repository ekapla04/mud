'''
    Class representing character object
'''
from threading import Lock

class Items:
    def __init__(self, name, desc, isVisible):
        self.__name = name
        self.__description = desc
        self.__isVisible = isVisible
        self.__mutex = Lock()
    
    def reaction(self):
        # callback for the item
        pass

    def getName(self):
        return self.__name

    def getDescription(self):
        return self.__description

    def setVisibility(self, value):
        with self.__mutex:
            self.__isVisible = value
    
    def isVisible(self):
        with self.__mutex:
            res = self.__isVisible

        return res
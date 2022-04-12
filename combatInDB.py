'''
    Class representing combat object
'''
from threading import Lock

class Combat:
    def __init__(self, fighter1, fighter2):
        self.__fighter1 = fighter1
        self.__fighter2 = fighter2
        self.__actions = {}
    
    def start(self):
        score1 = self.__fighter1.getHP() 
        score2 = self.__fighter2.getHP()

        while score1 > 0 or score2 > 0:
            # get action from fighter 1
            # get action from fighter 2
            # update score
            pass
        
        #updage hp for all players
        #end fight
    
    
'''
    Class representing combat object
'''
from threading import Lock
import asyncio



class Combat:
    def __init__(self, fighter1, fighter2):
        self.__fighter1 = fighter1
        self.__fighter1_ready = False
        self.__fighter1_numblock = 0

        self.__fighter2 = fighter2
        self.__fighter2_ready = False
        self.__fighter2_numblock = 0

        self.__actions = {}
        self.__actionsLock = Lock()
    
    async def start(self):
        winner = None
        loser  = None

        score1 = self.__fighter1.getHP()
        score2 = self.__fighter2.getHP()

        while winner is None:
            prompt = "Enter your move (block, ready, strike):"
            self.__fighter1.message(prompt)
            self.__fighter2.message(prompt)

            # Clear moves
            with self.__actionsLock:
                self.__actions = {}

            await asyncio.sleep(5)

            action_one = None
            action_two = None

            # Get player moves
            with self.__actionsLock:
                action_one = self.__actions.get(self.__fighter1)
                action_two = self.__actions.get(self.__fighter2)

            # Resolve moves
            print("actions received: ", self.__actions)

            # Deal with block
            # TODO: implement the limit on blocking
            if action_one == "block":
                if self.__fighter1_numblock >= 3:
                    self.__fighter1.message(f"You stumble, leaving yourself ungaurded. You can only block 3 times in a row.")
                    self.__fighter2.message(f"{self.__fighter1.get_name().capitalize()} stumbles when they try to block.")
                    action_one = "failed"
                else:
                    self.__fighter1_numblock += 1
                    self.__fighter1.message(f"You raise your thin sword to parry a strike.")
                
            if action_two == "block":
                if self.__fighter2_numblock >= 3:
                    self.__fighter2.message(f"You stumble, leaving yourself ungaurded. You can only block 3 times in a row.")
                    self.__fighter1.message(f"{self.__fighter2.get_name().capitalize()} stumbles when they try to block.")
                    action_one = "failed"
                else:
                    self.__fighter2_numblock += 1
                    self.__fighter2.message(f"You raise your thin sword to parry a strike.")

            # Deal with ready
            if action_one == "ready":
                self.__fighter1_ready = True
                self.__fighter1.message("You ready yourself to strike.")
                self.__fighter2.message(f"{self.__fighter1.get_name().capitalize()} gets ready to strike.")
                self.__fighter1_numblock = 0

            if action_two == "ready":
                self.__fighter2_ready = True
                self.__fighter2.message("You ready yourself to strike.")
                self.__fighter1.message(f"{self.__fighter2.get_name().capitalize()} gets ready to strike.")
                self.__fighter2_numblock = 0

            # Deal with attacks
            if action_one == "strike":   # Fighter 1
                if not self.__fighter1_ready:
                    self.__fighter1.message("You cannot strike with out first readying your attack.")
                elif action_two == "block":
                    self.__fighter1.message(f"{self.__fighter2.get_name()} blocks your strike.")
                    self.__fighter2.message(f"You parry {self.__fighter1.get_name()}'s strike.")
                else:
                    self.__fighter1.message(f"You strike {self.__fighter2.get_name()}.")
                    self.__fighter2.message(f"{self.__fighter1.get_name()} strikes you.")

                    self.__fighter2.decrementHP()
                    self.__fighter1_ready = False

                self.__fighter1_numblock = 0

            if action_two == "strike":   # Fighter 2
                if not self.__fighter2_ready:
                    self.__fighter2.message("You cannot strike with out first readying your attack.")
                elif action_one == "block":
                    self.__fighter2.message(f"{self.__fighter1.get_name()} blocks your strike.")
                    self.__fighter1.message(f"You parry {self.__fighter2.get_name()}'s strike.")
                else:
                    self.__fighter2.message(f"You strike {self.__fighter1.get_name()}.")
                    self.__fighter1.message(f"{self.__fighter2.get_name()} strikes you.")

                    self.__fighter1.decrementHP()
                    self.__fighter2_ready = False

                self.__fighter2_numblock = 0


            # Check for win condition (hp is at 0)
            if self.__fighter1.getHP() == 0 and self.__fighter2.getHP() == 0:
                winner = "draw"
            elif self.__fighter1.getHP() == 0:
                winner = self.__fighter2
                loser  = self.__fighter1
            elif self.__fighter2.getHP() == 0:
                winner = self.__fighter1
                loser  = self.__fighter2

        return {"winner": winner, "loser": loser}


    def is_in(self, character):
        if character.get_name() == self.__fighter1.get_name():
            return True

        if character.get_name() == self.__fighter2.get_name():
            return True

        return False
    
    def make_move(self, character, action):
        with self.__actionsLock:
            self.__actions[character] = action

    def list_fighters(self):
        return [self.__fighter1, self.__fighter2]

    def disconnect_character(self, character):
        """
            Call to end a fight early because Character character has disconnected
        """
        pass

    def is_ready(self, character):
        result = False
        with self.__actionsLock:
            if character == self.__fighter1:
                result = self.__fighter1_ready
            elif character == self.__fighter2:
                result = self.__fighter2_ready
        return result
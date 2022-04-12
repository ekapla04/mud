

class Command:
    def __init__(self, name, aliases, callback):
        self.__name = name
        self.__aliases = aliases
        self.__callback = callback

    def __do_nothing(self, character, args, server) :
        print("Do nothing called by", character, " doing nothing.")

    def execute(self, character, args, server):
        """
            execute - calls the command

            character - the character who is excecuting the command

            args - the arguments entered by the user

            server - the mud server
        """
        if self.__callback is None:
            self.__do_nothing(character, args, server)
        else:
            self.__callback(character, args, server)

    def is_this_command(self, word):
        """
            is_this_command - checks to see if the word matches any of the
                ways of refering to this command

            word - string, the phrase to check

            returns - True if the word and the command name/aliases match,
                and False otherwise
        """
        word = word.strip().lower()

        if word == self.__name.strip().lower():
            return True
        else:
            for alias in self.__aliases:
                if word == alias.strip().lower():
                    return True

        return False

    def get_name(self):
        return self.__name
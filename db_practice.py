from db import Database
from src.room import Room
from src.character import Character


def main():
    # create/open databases
    characters = Database("users.db")
    rooms = Database("rooms.db")

    # create room objects, add neighbors
    roomA = Room(21, "desert", "windy and dry")
    roomB = Room(34, "rainforest", "warm and humid")
    roomA.addNeighbor(roomB, "North")
    roomB.addNeighbor(roomA, "South")

    # add characters to database (in theory this is done upon creation of account)
    # integrity error seemingly not catching when i try to reload a previously 
    # seen user?
    characters.add_user(("sk","rw", "brunette", 21 ,"dog, cat, arrow","100"))
    characters.execute_users(("ek","ls", "blonde", 21 ,"dog, cat, arrow","100"))
    characters.execute_users(("mj","ilovepurple", "ginger", 34 ,"dog, cat, arrow","100"))
    characters.commit()

    # create character objects, add them to rooms
    characterA = Character("ek", "ls", "tall and blonde", 21)
    characterB = Character("sk", "rw", "brunette with brown eyes", 21)
    characterC = Character("mj","ilovepurple", "ginger", 34)
    roomA.addCharacter(characterA)
    roomA.addCharacter(characterB)
    roomB.addCharacter(characterC)

    # load room objects into database... already done, so comment out to avoid
    # integrity error... will crash if try to reload it, maybe use try-catch?
    # rooms.load_room(roomA)
    # rooms.load_room(roomB)
    rooms.commit()

    # retrieve room objects from database
    roomC = rooms.retrieve_room((21))
    print(roomC.getDisplayName())

main()

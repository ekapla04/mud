import sys
sys.path.insert(0, '/h/ekapla04/comp21/mud/src')
from db import Database
from room import Room
from character import Character
from items import Items


def main():
    # create/open databases
    characters = Database("users.db")
    rooms = Database("rooms.db")
    items = Database("items.db")


    # create room objects, add neighbors
    roomA = Room(21, "desert", "windy and dry")
    roomB = Room(34, "rainforest", "warm and humid")
    roomC = Room(48, "winter wonderland", "cold and snowy")
    roomA.addNeighbor(roomB, "North")
    roomB.addNeighbor(roomA, "South")
    roomC.addNeighbor(roomB, "West")
    roomC.addNeighbor(roomA, "East")


    # add characters to database (in theory this is done upon creation of account)
    # integrity error seemingly not catching when i try to reload a previously 
    # seen user?
    # characters.add_user(("pw","nyc", "blonde", 21 ,"dog, cat, arrow","100"))
    # characters.add_user(("janine","swimlover", "gray hair", 21 ,"dog, cat, arrow","100"))
    # characters.add_user(("janice","camping123", "black hair", 21 ,"dog, cat, arrow","100"))
    # characters.add_user(("janet","cooldog", "brunette", 21 ,"dog, cat, arrow","100"))
    # characters.add_user(("sk","rw", "brunette", 21 ,"dog, cat, arrow","100"))
    # characters.execute_users(("ek","ls", "blonde", 21 ,"dog, cat, arrow","100"))
    # characters.execute_users(("mj","ilovepurple", "ginger", 34 ,"dog, cat, arrow","100"))
    # characters.commit()

    # create character objects, add them to rooms
    characterA = Character("ek", "ls", "tall and blonde", 21)
    characterB = Character("sk", "rw", "brunette with brown eyes", 21)
    characterC = Character("mj","ilovepurple", "ginger", 34)
    characterD = Character("ella","enchanted", "ginger", 34)
    roomA.addCharacter(characterA)
    roomA.addCharacter(characterB)
    roomB.addCharacter(characterC)

    itemA = Items("sock", "purple with polkadots", True, "ek")
    # items.add_item(("sock", "purple with polkadots", "True", "ek"))
    items.add_item(itemA)

    itemB = Items("backpack", "holds magic coin", True, "ella")
    items.add_item(itemB)

    characterD.addToInventory(itemA)
    characterD.addToInventory(itemB)

    characters.add_user(characterD)
    boolA, resultA = items.in_items(("backpack", "ella"))
    boolB, resultB = items.in_items(("barkpik", "ella"))
    boolC, resultC = items.in_items(("backpack", "ells"))
    print(resultB)
    print(resultC)

    # load room objects into database... already done, so comment out to avoid
    # integrity error... will crash if try to reload it, maybe use try-catch?
    # rooms.load_room(roomA)
    # rooms.load_room(roomB)
    # rooms.load_room(roomC)
    # rooms.commit()

    # retrieve room objects from database
    roomC = rooms.retrieve_room((21))
    # print(roomC.getDisplayName())
    # print(roomC.getExits())
    print(roomC.getIn)
    returned_rooms = rooms.return_all_rooms()
    # print(returned_rooms)


main()

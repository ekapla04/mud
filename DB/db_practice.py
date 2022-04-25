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

    # create character objects, add them to room objects
    characterA = Character("ek", "ls", "tall and blonde", 21)
    characterB = Character("sk", "rw", "brunette with brown eyes", 21)
    characterC = Character("mj","ilovepurple", "ginger", 34)
    characterD = Character("ella","enchanted", "ginger", 34)
    roomA.addCharacter(characterA)
    roomA.addCharacter(characterB)
    roomB.addCharacter(characterC)


    # create item object, add it to database
    itemA = Items("sock", "purple with polkadots", True, "ek")
    items.add_item(itemA)

    itemB = Items("backpack", "holds magic coin", True, "ella")
    items.add_item(itemB)

    itemC = Items("rock", "smooth and shiny", True, "ek")
    items.add_item(itemC)

    # add inventory to character object
    characterD.addToInventory(itemA)
    characterD.addToInventory(itemB)

    # add character objects to database
    characters.add_user(characterD)
    characters.add_user(characterA)
    characters.add_user(characterB)
    characters.add_user(characterC)
    boolA, resultA = items.in_items(("backpack", "ella"))
    boolB, resultB = items.in_items(("barkpik", "ella"))
    boolC, resultC = items.in_items(("backpack", "ells"))
    # print(resultB)
    # print(resultC)

    # for this to be a meaningful update, item object should have been created
    # and added to datebase with user it's intended for
    characters.update_user_items("ek", "sock")
    characters.update_user_items("ek", "rock")

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
    # print(roomC.getIn)
    returned_rooms = rooms.return_all_rooms()
    print(returned_rooms)


main()

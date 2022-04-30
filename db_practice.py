from db import Database
from src.room import Room
from src.character import Character
from src.items import Items


def main():
    # create/open databases
    characters = Database("users.db")
    rooms = Database("rooms.db")
    items = Database("items.db")


    # create room objects
    roomA = Room(21, "desert", "windy and dry")
    roomB = Room(34, "rainforest", "warm and humid")
    roomC = Room(48, "winter wonderland", "cold and snowy")

    # add neighbors to room objects
    roomA.addNeighbor(roomB, "North")
    roomA.addNeighbor(roomC, "West")
    roomB.addNeighbor(roomA, "South")
    roomC.addNeighbor(roomB, "West")
    roomC.addNeighbor(roomA, "East")

    # create character objects
    characterA = Character("ek", "ls", "tall and blonde", 21)
    characterB = Character("sk", "rw", "brunette with brown eyes", 21)
    characterC = Character("mj","ilovepurple", "ginger", 34)
    characterD = Character("ella","enchanted", "ginger", 34)

    # add characters to room objects
    roomA.addCharacter(characterA)
    roomA.addCharacter(characterB)
    roomB.addCharacter(characterC)


    # create item object
    itemA = Items("sock", "purple with polkadots", True, "ek")
    itemB = Items("backpack", "holds magic coin", True, "ella")
    itemC = Items("rock", "smooth and shiny", True, "ek")
    itemD = Items("rock", "smooth and shiny", True, "21")
    itemE = Items("backpack", "holds magic coin", True, "21")


    # add item to items database
    items.add_item(itemA)
    items.add_item(itemB)
    items.add_item(itemC)
    items.add_item(itemD)
    items.add_item(itemE)

    in_items, item_result = items.in_items("backpack", "21")
    # print(item_result)

    items.delete_item_from_items("backpack", "21")
    in_items, item_result = items.in_items("backpack", "21")
    print(item_result)

    # add item to room object (this must happen in addition to item being added
    # to room entry in room DB... item can be added to room entry two different 
    # ways:
    #   if room has been loaded already --> update_room_items
    #   if room has not been added to DB yet --> load_room will automatically 
    #   add it to room's DB entry)
    roomA.addItems(itemD)

    # roomA.addItems(itemE)

    # add inventory to character object --> we know this belongs to characterD
    # because D's username is "ek" which is the specified owner of the item 
    # in the item object
    characterD.addToInventory(itemA)
    characterD.addToInventory(itemB)

    # add character objects to database
    characters.add_user(characterD)
    characters.add_user(characterA)
    characters.add_user(characterB)
    characters.add_user(characterC)

    # function to retrieve item names in a user's inventory
    # boolA, resultA = items.in_items("backpack", "ella")
    # boolB, resultB = items.in_items("barkpik", "ella")
    # boolC, resultC = items.in_items("backpack", "ells")
    # print(resultB)
    # print(resultC)

    # for this to be a meaningful update, item object should have been created
    # and added to datebase with user it's intended for
    # characters.update_user_items("ek", "sock")
    # characters.update_user_items("ek", "rock")

    # characters.delete_user("ek")
    # characters.delete_user_from_users("ek")
    bool, ek = characters.in_users("ek")
    print(ek)

    # rooms.add_user_to_room("ek", "21")

    # characters.delete_item_from_users("sock", "ek")
    # bool, ek = characters.in_users("ek")
    # print(ek)


    # load room objects into database... already done, so comment out to avoid
    # integrity error... will crash if try to reload it, maybe use try-catch?
    # rooms.delete_room(21)
    # rooms.delete_room(34)
    rooms.load_room(roomA)
    rooms.load_room(roomB)
    # rooms.load_room(roomB)
    # rooms.load_room(roomC)
    rooms.commit()

    # update room's items after room has been added to DB already
    rooms.update_room_items(21, itemE)

    bool, roomInfo = rooms.in_rooms(21)
    print("room before change user 21: " + str(roomInfo))

    bool, roomInfo = rooms.in_rooms(34)
    print("room before change user 34: " + str(roomInfo))

    characters.change_user_room("ek", 34)
    # rooms.delete_user_from_room("ek",21)
    # rooms.add_user_to_room("ek",34)
    rooms.room_swap(21, 34, "ek",)

    bool, roomInfo = rooms.in_rooms(21)
    print("room after change user 21: " + str(roomInfo))

    bool, roomInfo = rooms.in_rooms(34)
    print("room after change user 34: " + str(roomInfo))

    bool, ek = characters.in_users("ek")
    print("ek user updated: " + str(ek))


    # test function to delete room entry
    # rooms.delete_room(21)

    # test function to delete user from room entry
    # rooms.delete_user_from_room("ek", 21)


    # for some reason overwriting this
    # rooms.update_room_characters(21, "cat")
    # bool, roomInfo = rooms.in_rooms(21)
    # print("room info1: " + str(roomInfo))

    # updates room characters --> for this to be meaningful, "emma" should be 
    # a user in the user DB
    # rooms.update_room_characters(21, "emma")


    # retrieve room objects from database
    roomD = rooms.retrieve_room(21)
    # printing to ensure correct data was retrieved
    # print("room D display name: " + str(roomD.getDisplayName()))
    # print("room D characters: " + str(roomD.getCharacters()))
    # print("room D exits: " + str(roomD.getExits()))
    # print("room D items: " + str(roomD.getItems()))

    # list of room objects stored in DB
    # returned_rooms = rooms.return_all_rooms()
    # print(returned_rooms)


main()


############## NOTES ##############
# character must be in character db before being added to room
# 
#
#
#
#
#

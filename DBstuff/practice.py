from yaml import parse
from user_db import *
from room_db import *

def main():
    # user_example()
    room_example()

def user_example():
    print("######### USER EXAMPLE #########")
    # create/open user database
    users = UserDatabase()

    # add users to table
    users.executemany(("ek","ls","forest","nothing, car, hello","100",))
    users.executemany(("wl","ts","desert","dog, cat, arrow","100",))

    # commits new data to db
    users.commit()

    # checks if user is in table using username/password
    boolean,result = users.in_table(("ek"))
    if boolean == True:
        print("user in table: " + str(result) + "\n")
    
    # retrieve user inventory 
    inventory_ek = users.parse_inventory("ek")
    print("ek inventory: " + str(inventory_ek) + "\n")

    # retrieve user inventory of someone not in table
    inventory_wq = users.parse_inventory("wq")
    print("wq inventory: " + str(inventory_wq) + "\n")

    # test on user not in table
    users.in_table(("wq","ts"))

def room_example():
    rooms = RoomDatabase()

    # manually add room to database
    rooms.executemany(("21", "Black Forest", "Dark and gloomy", \
                    "north, south", "ek, ws, user123",))
    rooms.executemany(("38", "White River Junction", "Snowy overpass", \
                    "north, east", None,))

    rooms.commit()

    # checking that room was successfully added and can be retrieved
    data = rooms.in_table(("21", "Black Forest"))
    print("retrieved data: " + str(data) + "\n")


    # test on room not in table
    data = rooms.in_table(("21", "Waterfall"))
    print("retrieved data: " + str(data) + "\n")

    exits = rooms.parse_information(("21", "Black Forest"), "exits")
    print("exits in Black Forest: " + str(exits))

    characters = rooms.parse_information(("21", "Black Forest"), "characters")
    print("characters in Black Forest: " + str(characters) + "\n")

    # import data via file csv
    rooms.import_data("room.csv")

    rooms.commit()

    exits = rooms.parse_information(("31", "Forbidden Forest"), "exits")
    print("exits in Forbidden Forest: " + str(exits))




main()

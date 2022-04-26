import sqlite3
from db import Database
from src.room import Room

db = Database("game.db")
db.create_roomDB()
db.create_userDB()

# uui, name, description, exits, characters

atrium = Room("atrium", "Atrium", """A two story tall atrium with grand windows, \
    a central fountain and an excess of green leafy plants.""")
mainhall = Room("mainhall", "Main Hall", """A large, extravagant entry hall.\
    The walls are mirrored and at the far end is a large sliding glass door.""")

atrium.addNeighbor(mainhall, "south")

mainhall.addNeighbor(atrium, "north")


print("loading rooms")

try:
    db.load_room(mainhall)
    db.load_room(atrium)
except sqlite3.IntegrityError as e:
    print("Room's already loaded")

print("rooms loaded")

db.commit()

db.retrieve_room(("atrium"))


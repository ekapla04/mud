from db import Database
from src.room import Room

DB = Database("game.db")

DB.create_roomDB()
DB.create_userDB()

# make a temporary map


atrium = Room("atrium", "Atrium", """A two story tall atrium with grand windows, \
    a central fountain and an excess of green leafy plants.""")
mainhall = Room("mainhall", "Main Hall", """A large, extravagant entry hall.\
    The walls are mirrored and at the far end is a large sliding glass door.""")
sittingroom = Room("sittingroom", "Sitting Room", """A lush sitting room with \
luminescent green couches. An intricte portrait of a young woman hangs above the mantle. """)
courtyard = Room("courtyard", "Cout Yard", """ A small court yard tiled with rough gray stones \
    arranged in circular patterns around a small fountain.""")


atrium.addNeighbor(mainhall, "south")
mainhall.addNeighbor(atrium, "north")
atrium.addNeighbor(sittingroom, "east")
sittingroom.addNeighbor(atrium, "west")

sittingroom.addNeighbor(courtyard, "north")
courtyard.addNeighbor(sittingroom, "south")



DB.load_room(atrium)
DB.load_room(mainhall)
DB.load_room(sittingroom)
DB.load_room(courtyard)

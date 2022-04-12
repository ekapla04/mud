from character import Character
from command import Command
from room import Room


# ================= LOOK ======================
def _look_callback(character: Character, args, server):
    """
        Message the user the description of the current room + it's contents
    """
    location =  character.getLocation()

    # If no arguments are given, send the room description
    if len(args) == 0:
        roomdesc = f""" === {location.getDisplayName()} ===
        {location.getDescription()}
        """
        character.message(roomdesc)
        # TODO: Add contents

    else:
        character.message("look at not yet implemented")
        # TODO: If args are given attempt to describe the corresponding object

look = Command("look", ["l"], _look_callback)


# ================= PING ======================
def _ping_callback(character: Character, args, server):
    character.message("pong")


ping = Command("ping", [], _ping_callback)


# ================= SAY ======================

def _say_callback(character: Character, args, server):
    if len(args) < 1:
        character.message("Usage: say message")
        return

    tosay = " ".join(args).strip().strip("\"").capitalize()

    # Determine how the sentence is being said
    mode_of_speech = ("say", "says")
    if tosay.endswith("?"):
        mode_of_speech = ("ask", "asks")
    elif tosay.endswith("!"):
        mode_of_speech = ("exclaim", "exclaims")
    else:
        if not tosay.endswith("."):
            tosay += "."

    # Message the sender
    character.message(f"You {mode_of_speech[0]}: \"{tosay}\"")

    # Message everyone else in the room
    character.message_location(f"{character.get_name().capitalize()} {mode_of_speech[1]}: \"{tosay}\"")


say = Command("say", [], _say_callback)

# Define functions to export those objects as command sets
def default_cmd_set():
    return {ping.get_name(): ping,
            look.get_name(): look,
            say.get_name(): say}

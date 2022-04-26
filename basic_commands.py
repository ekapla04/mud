from src.character import Character
from src.command import Command
from src.room import Room
from src.combat import Combat
import interactionutils as utils


# ================= LOOK ======================
async def _look_callback(character, args, gamestate):
    """
        Message the user the description of the current room + it's contents
    """
    location =  character.getLocation()

    # If no arguments are given, send the room description
    if len(args) == 0:
        # Get the exit names
        exits = location.getExits()
        exit_text = "Exits: "
        print(list(exits.keys()))
        if len(exits.keys()) == 0 :
            exit_text += "None"
        else:
            keys = list(exits.keys())
            exit_text += ", ".join(keys)

        chars = list(location.getCharacters().keys())
        char_text = "Characters: "
        print("chars in room: ", chars)
        if len(chars) == 0:
            char_text += "None"
        else:
            char_text += ", ".join(chars)



        roomdesc = f""" === {location.getDisplayName()} === <br>
        {location.getDescription()} <br>
        {exit_text} <br>
        {char_text}
        """
        character.message(roomdesc)


        # TODO: Add contents

    else:
        character.message("look at not yet implemented")
        # TODO: If args are given attempt to describe the corresponding object

look = Command("look", ["l"], _look_callback)


# ================= PING ======================
async def _ping_callback(character, args, gamestate):
    character.message("pong")


ping = Command("ping", [], _ping_callback)


# ================== SAY ======================

async def _say_callback(character, args, gamestate):
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


# ================== MOVE ======================
async def _move_callback(character, args, gamestate):
    if character.is_fighting():
        character.message(f"You cannot leave the room until you finish your duel.")
        return

    # User must provide the name of an exit
    if len(args) == 0:
        character.message("Usage: move exit")
        return

    args = " ".join(args)

    location = character.getLocation()

    exits = location.getExits()

    if args.lower() in exits:
        destination = exits[args.lower()]

        # Alert the people in the current room that they left
        character.message_location(f"{character.get_name().capitalize()} moves {args.lower()}.")

        # Move the character
        location.removeCharacter(character)
        destination.addCharacter(character)
        character.setLocation(destination)
        
        # Alert the people in the destination room that they arrived
        character.message_location(f"{character.get_name().capitalize()} enters.")

        # Look at the destination
        await _look_callback(character, [], gamestate)
    else:           # The exit does not exist here :(
        character.message(f"{args.capitalize()} is not an exit.")


move = Command("move", [], _move_callback)


# ================== COMMANDS ======================
async def _commands_callback(character, args, gamestate):
    """
        Lists all the commands available to the user
    """
    commands = list(character.get_commands().keys())
    character.message(f"Avilable commands: {', '.join(commands)}")


commands = Command("commands", [], _commands_callback)

# ================== MAP ======================
async def _map_callback(character, args, gamestate):
    character.message("You asked for a map...", "map")

    max_depth = 3

    arr = [[0 for i in range(max_depth)] for j in range(max_depth)]
    pass

show_map = Command("map", [], _map_callback)


# =========================================================
# ==                COMBAT COMMANDS                      ==
# =========================================================

# ================== CHALLENGE ======================
async def _challenge_callback(character, args, gamestate):
    if len(args) != 1 :
        character.message("Usage: challenge character name")
        return

    location = character.getLocation()

    # Check if that character is in the room
    if character.get_name() == args[0].lower():
        character.message("You cannot duel yourself.")
        return

    if not location.isPresent(args[0].lower()):
        character.message(f"{args[0].lower().capitalize()} is not here.")
        return

    # Check if they are in a duel already
    opponent = gamestate.get_character(args[0].lower())
    if opponent is None:
        character.message(f"{args[0].lower().capitalize()} cannot be found and has probably left.")
        return

    if location.is_fighting(opponent):
        character.message(f"{opponent.get_name()} is already dueling.")
        return


    # Set both characters to fighting so they cannot leave the room
    character.set_is_fighting(True)
    opponent.set_is_fighting(True)

    # Challenge them
    character.message(f"You throw down your glove and challenge {opponent.get_name().capitalize()} to a duel.")
    opponent.message(f"{character.get_name().capitalize()} challenges you to a duel. <br> Do you accept?")

    response = await utils.get_yes_no(opponent)
    print("response = ", response, f", character {character.get_name()}, opponent {opponent.get_name()}")

    # Case where they decline
    if response == "no":
        character.message(f"{opponent.get_name().capitalize} declines your challenge.")
        opponent.message(f"You decline {character.get_name().capitalize()}'s challenge.")
        character.set_is_fighting(False)
        opponent.set_is_fighting(False)

    # Case where they accept
    else:
        character.message(f"{opponent.get_name().capitalize()} accepts your challenge.")
        opponent.message(f"You accept {character.get_name().capitalize()}'s challenge.")

        # Create the combat object
        combat = Combat(character, opponent)
        location.addCombat(combat)
        result = await combat.start()
        if result == "draw":
            location.broadcast_all(f"{character.get_name.capitalize()} and {opponent.get_name.capitalize()} both fall to their knees. The duel is a draw.")
        else:
            location.broadcast_all(f"{result['winner'].get_name().capitalize()} defeats {result['loser'].get_name().capitalize*()} in a duel.")

        character.set_is_fighting(False)
        opponent.set_is_fighting(False)

challenge = Command("challenge", ["duel"], _challenge_callback)

# ================== STRIKE ======================
async def _strike_callback(character, args, gamestate):
    location = character.getLocation()

    if not location.is_fighting(character):
        character.message("You are not in a duel. You cannot strike.")
        return

    combat = location.getCombat(character)
    combat.make_move(character, "strike")



strike = Command("strike", ["hit"], _strike_callback)


# ================== BLOCK ======================
async def _block_callback(character, args, gamestate):
    location = character.getLocation()

    if not location.is_fighting(character):
        character.message("You are not in a duel. You cannot block.")

    combat = location.getCombat(character)
    combat.make_move(character, "block")

block = Command("block", [], _block_callback)


# ================== READY ======================
async def _ready_callback(character, args, gamestate):
    location = character.getLocation()

    if not location.is_fighting(character):
        character.message("You are not in a duel. You cannot ready an attack.")

    combat = location.getCombat(character)
    combat.make_move(character, "ready")

ready = Command("ready", [], _ready_callback)


async def _ask_callback(character, args, gamestate):
    print(await utils.get_yes_no(character))

ask = Command("ask", [], _ask_callback)





# Define functions to export those objects as command sets
def default_cmd_set():
    return {ping.get_name():      ping,
            look.get_name():      look,
            say.get_name():       say,
            move.get_name():      move, 
            commands.get_name():  commands,
            show_map.get_name():  show_map,
 
            challenge.get_name(): challenge,
            strike.get_name():    strike,
            block.get_name():     block,
            ready.get_name():     ready,
            ask.get_name(): ask}

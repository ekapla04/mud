import sys
sys.path.append("pypackages")
sys.path.append("../src")

import websockets
import asyncio
import json

from gamestate import GameState

GAMESTATE = None


async def echo(websocket):
    try:
        async for message in websocket:
            print(f"<<< {websocket.remote_address} says: {message}")
            websockets.broadcast({websocket}, message.upper())
    finally:
        print("Client disconnected")


async def login(websocket):
    global GAMESTATE
    char_name = ""

    def reprompt():
        tosend = {"type": "err", "text": f"Bad login string. \n Must be of form login or create // name // pass [// room]"}        
        websockets.broadcast({websocket}, json.dumps(tosend))

    def message_character(msg):
        websockets.broadcast({websocket}, msg)

    try:
        async for message in websocket:
            message = message.split("//")


            if len(message) < 3:
                reprompt()
                continue
            
            if message[0].strip().lower() == "login":
                code = GAMESTATE.connect_character(message[1].strip().lower(), message[2].strip(), websocket)
                if code != "ok":
                    reprompt()
                    continue
            elif message[0].strip().lower() == "create":
                if len(message) != 4:
                    reprompt()
                    continue

                password = message[2].strip()
                if password != password:  # TODO: validate password correctly!
                    reprompt()
                    continue

                code = GAMESTATE.create_character(message[1].strip().lower(), message[2].strip(), message[3].strip().lower(), websocket)

                if code != "ok":
                    reprompt()
                    continue

            char_name = message[1].strip().lower()

            break
    finally:
        pass

    return char_name

def parse_command(text):
        """
            parse_command - breaks the command into command word and arguments
            text - non-empty, non-whitespace string representing the user's input
            returns - a tuple of the form ("command", ["list", "of", "args"])
        """
        text = text.strip().split()
        command = text[0]
        text.pop(0)
        return (command, text)

def execute_command(character, command, args):
    """
        execute_command - excecutes the given command
        TODO - Make it do the thing!
    """
    global GAMESTATE
    print(command, args)

    found = False
    cmd_set = character.get_commands()
    for cmd in cmd_set.values():
        if cmd.is_this_command(command):
            found = True
            cmd.execute(character, args, GAMESTATE)
            # print(f"Called execute on command {command}")

    if not found:
        print("command not found, try movement")
        # update found if movement is possible

    if not found:
        print("no exits, unknown command!")


    # self.send_msg(f"command: {command} with args: {args}")


# ==================== CONNECTION HANDLER ====================

async def MudConnection(websocket,dummy):
    global GAMESTATE
    char_name = ""

    try:
        await websocket.send(json.dumps({"type": "msg", "text":"Enter login string:"}))
        # Login character
        char_name = await login(websocket)
        char = GAMESTATE.get_character(char_name)
        await websocket.send(json.dumps({"type":"msg", "text":f"Logged in as {char_name}!"}))

        # Main game loop

        async for message in websocket:
            # The user wants to quit
            if message == "quit":
                print(message)
                websockets.broadcast({websocket}, message.upper())
                break

            # It's a command! Parse it >:)
            cmd, args = parse_command(message)
            
            execute_command(char, cmd, args)


    finally:
        print(f"{char_name} disconnected.")


# ==================== MAIN ====================

async def main():
    global GAMESTATE
    GAMESTATE = GameState("nowhere")

    async with websockets.serve(MudConnection, "localhost", 8001):

        await asyncio.Future()  # run forever


if __name__ == "__main__":

    asyncio.run(main())
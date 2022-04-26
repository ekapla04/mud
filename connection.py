import asyncio


class Connection():
    def __init__(self, character, websocket):
        self.character = character
        self.websocket = websocket
        self.doing_commands = True
        self.message_queue = asyncio.Queue()
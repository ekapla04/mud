import sys
sys.path.append("pypackages")

import websockets
import asyncio
import json


async def get_response_from(char, options, prompt="", case_sensitive=False):
    """
        Prompts the user for a specific response from an options dictionary

        options - dictionary of the form {"resp" : {aliases, set}, ...}
        
        prompt - reprompt the user if they respond incorrectly
    """
    # If not case sensitive, lower options 
    if not case_sensitive:
        options =  {key.lower(): val for key, val in options.items()}
        for key in options.keys():
            new = {None}
            for item in options[key]:
                new.add(item.lower())
            new.remove(None)
            options[key] = new

    print(options)

        

    choice = None
    try:
        char.doing_commands = False
        while choice is None:
            message = ""
            try:
                message = await char.message_queue.get()
            except:
                continue


            if not case_sensitive:
                message = message.lower()

            for key in options.keys():
                if key == message:
                    choice = key
                    break
                elif message in options[key]:
                    choice = message
                    break
                
            if not choice is None:
                break
            else:
                if prompt == "":
                    ops = ", ".join(list(options.keys()))
                    prompt = f"Enter one of: {ops}."
                await char.websocket.send(json.dumps({"type": "err", "text": prompt}))

            

    finally:
        print(f"chose: {choice}")
        char.doing_commands = True

    return choice

async def get_yes_no(charion):
    """
        Prompts the user to respond with yes or no
    """
    response = await get_response_from(charion, {"yes": {"y"}, "no": {"n"}}, prompt="Answer yes or no")
    return response

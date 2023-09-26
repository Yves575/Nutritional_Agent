import asyncio
from rasa.core.agent import Agent
from furhat_remote_api import FurhatRemoteAPI
import requests

# Load trained model
agent = Agent.load('models/20230921-055753-lazy-dailies.tar.gz')

# Initialize Furhat
furhat = FurhatRemoteAPI("localhost")
furhat.set_voice(name='Matthew')

async def handle_user_interaction():
    # furhat.gesture(name="smile")
    prev_r = None
    furhat.say(text='Hello! How can I assist you with your nutrition today?', blocking=True)

    while True:
        # Get the user's speech input
        speech_input = (furhat.listen())
        print(speech_input)
        if (speech_input.message != ""):
            print("Here what is said: %s" %(speech_input.message))
            
            # Handle user input
            #responses = await agent.handle_text(speech_input.message)
            url = "http://localhost:5005/webhooks/rest/webhook"
            payload = {
            "sender": "user1",
            "message": speech_input.message
            }

            r = requests.post(url, json=payload)
            print(r.json, prev_r)
            if (prev_r == None) or (r.json() != prev_r):
                for i in r.json():
                    bot_message = i['text']
                    furhat.say(text=f"{i['text']}")
                    prev_r = r.json()
    
    furhat.say(text='Goodbye! Stay healthy and eat well!')
    # furhat.gesture(name="smile")

# Run the interaction
loop = asyncio.get_event_loop()
loop.run_until_complete(handle_user_interaction())
loop.close()
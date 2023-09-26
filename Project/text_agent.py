from rasa.core.agent import Agent
import asyncio
import requests

# This asynchronous function loads a trained Rasa model to create an agent.
async def load_agent():
    model_path = 'models/20230804-144142-gray-lighting.tar.gz'
    endpoints_path = 'endpoints.yml'
    agent = Agent.load(model_path, action_endpoint=endpoints_path)
    return agent

# This asynchronous function handles interactions with the user using the loaded agent.
async def handle_user_interaction():
    agent = await load_agent()
    bot_message = ""
    print("Bot is ready to talk! Type 'stop' to end the conversation.")
    
    while True:
        # Get user input
        user_message = input("You: ")
        
        # If user types 'stop', end the conversation.
        if user_message.lower() == 'stop':
            print("Conversation ended.")
            break
        url = "http://localhost:5005/webhooks/rest/webhook"
        payload = {
        "sender": "user1",
        "message": user_message
        }

        # Make a POST request to the Rasa server with the payload.
        r = requests.post(url, json=payload)

        # Process the response from the server and print bot's messages.
        for i in r.json():
            bot_message = i['text']
            print(f"{i['text']}")

# Run the interaction loop
loop = asyncio.get_event_loop()
loop.run_until_complete(handle_user_interaction())

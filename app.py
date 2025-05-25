import os
from aiohttp import web  # For creating the web server
from dotenv import load_dotenv
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings  # Adapter to connect bot to Azure
from botbuilder.schema import Activity  # Represents incoming bot messages
from bot import MyBot

load_dotenv()

APP_ID = os.getenv("microsoft_app_id", "")
APP_PASSWORD = os.getenv("microsoft_app_password", "")

# Create adapter settings using app credentials
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
# Create an adapter instance to handle messages between Azure and your bot
adapter = BotFrameworkAdapter(adapter_settings)

# Create an instance of your bot
bot = MyBot()

# This function handles incoming HTTP POST requests from Azure to /api/messages
async def messages(req: web.Request) -> web.Response:
    body = await req.json()  # Get the request body as JSON
    activity = Activity().deserialize(body)  # Convert JSON into an Activity object
    auth_header = req.headers.get("Authorization", "")  # Extract auth token if any

    # Pass the activity to the adapter, which will forward it to your bot's logic
    response = await adapter.process_activity(activity, auth_header, bot.on_turn)

    # If the bot returns a response, send it back to the client
    if response:
        return web.json_response(data=response.body, status=response.status)

    # Otherwise, return a success status
    return web.Response(status=201)

app = web.Application()

# Route incoming POST requests to /api/messages to the messages handler
app.router.add_post("/api/messages", messages)

# Start the web server on localhost
if __name__ == "__main__":
    try:
        web.run_app(app, host="localhost", port=3978)
    except Exception as error:
        raise error

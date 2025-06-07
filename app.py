import os
from aiohttp import web
from dotenv import load_dotenv
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from bot import MyBot

load_dotenv()

APP_ID = os.getenv("microsoft_app_id", "")
APP_PASSWORD = os.getenv("microsoft_app_password", "")

adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

bot = MyBot()

async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    if response and hasattr(response, "body"):
        return web.json_response(data=response.body, status=response.status)
    else:
        return web.Response(text="Bot handled message.", status=200)


app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(app, host="localhost", port=3978)
    except Exception as error:
        raise error

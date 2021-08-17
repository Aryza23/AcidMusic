import requests
from pyrogram import Client as Bot

from AcidMusic.config import API_HASH
from AcidMusic.config import API_ID
from AcidMusic.config import BG_IMAGE
from AcidMusic.config import BOT_TOKEN
from AcidMusic.services.callsmusic import run

response = requests.get(BG_IMAGE)
file = open("./etc/foreground.png", "wb")
file.write(response.content)
file.close()

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="AcidMusic.modules"),
)

bot.start()
run()

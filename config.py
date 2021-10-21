import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
que = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Aries")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/ccdb7dd3392bc90248472.jpg")
THUMB_IMG = getenv("THUMB_IMG", "https://telegra.ph/file/257c2b28860112a84d985.jpg")
AUD_IMG = getenv("AUD_IMG", "https://telegra.ph/file/257c2b28860112a84d985.jpg")
QUE_IMG = getenv("QUE_IMG", "https://telegra.ph/file/257c2b28860112a84d985.jpg")
admins = {}
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_USERNAME = getenv("BOT_USERNAME", "idzeroid_bot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "idzxmusic")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "idzeroidsupport")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "idzeroid")
OWNER_NAME = getenv("OWNER_NAME", "idzxartez") # isi dengan username kamu tanpa simbol @
DEV_NAME = getenv("DEV_NAME", "idzxartez")
PMPERMIT = getenv("PMPERMIT", None)
DATABASE_URL = getenv("DATABASE_URL", "mongodb+srv://kentot:kentot@cluster0.7mbhj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "90"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))

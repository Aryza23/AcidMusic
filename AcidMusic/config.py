import os
from os import path
from os import getenv
from dotenv import load_dotenv
from helpers.modhelps import fetch_heroku_git_url


if os.path.exists("local.env"):
    load_dotenv("local.env")

que = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "idzero_gr")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/85fb675d640dd1feb8063.png")
admins = {}
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH")
BOT_USERNAME = getenv("BOT_USERNAME")
# Your Telegram User ID
OWNER = int(getenv("OWNER"))
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "Idzeroobot")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "idzero_gr")
PROJECT_NAME = getenv("PROJECT_NAME", "AcidMusic")
SOURCE_CODE = getenv("SOURCE_CODE", "github.com/idzero23/AcidMusic")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "15"))
ARQ_API_KEY = getenv("ARQ_API_KEY", None)
PMPERMIT = getenv("PMPERMIT", None)
LOG_GRP = getenv("LOG_GRP", None)
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
# Updator Configs
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)
HEROKU_API_KEY = getenv("HEROKU_API_KEY", None)
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/idzero23/AcidMusic")
U_BRANCH = "main"
HEROKU_URL = fetch_heroku_git_url(HEROKU_API_KEY, HEROKU_APP_NAME)

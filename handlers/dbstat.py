import os
import time
import string
import random
import asyncio
import aiofiles
import datetime
from AcidMusic.utils.database import Database
from Acidmusic main import bot
from AcidMusic.vars import Var
from pyrogram import filters, Client
from pyrogram.types import Message
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)



@bot.on_message(filters.command("status") & filters.private & filters.user(Var.OWNER_ID) & ~filters.edited)
async def sts(c: Client, m: Message):
    total_users = await db.total_users_count()
    await m.reply_text(text=f"**Total Users in DB:** `{total_users}`", parse_mode="Markdown", quote=True)

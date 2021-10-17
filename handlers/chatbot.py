import re
import aiohttp
import requests
import asyncio


from pyrogram import filters
from time import time
from main import bot
import AcidMusic.handlers.sql.kuki_sql as sql


BOT_ID = 1914584978

@bot.on_message(
    filters.command(["addchat", f"addchat@idzeroid_bot"])
)
async def addchat(_, message):
    chid = message.chat.id
    is_kuki = sql.is_kuki(chid)
    if not is_kuki:
        sql.set_kuki(int(message.chat.id))
        m.reply_text(
            f"kuki AI Successfully {message.chat.id}"
        )
    await asyncio.sleep(5)

@bot.on_message(
    filters.command(["rmchat", f"rmchat@idzeroid_bot"])
)
async def rmchat(_, message):
    chid = message.chat.id
    is_kuki = sql.is_kuki(chid)
    if not is_kuki:
        sql.rm_kuki(int(message.chat.id))
        m.reply_text(
            f" AI disabled successfully {message.chat.id}"
        )
    await asyncio.sleep(5)


@bot.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def kuki(_, message):
    try:
        chid = message.chat.id
        is_kuki = sql.is_kuki(chid)
        if not is_kuki:
            return
        if not message.reply_to_message:
            return
        try:
            moe = message.reply_to_message.from_user.id
        except:
            return
        if moe != BOT_ID:
            return
        text = message.text
        Kuki = requests.get(f"https://www.kukiapi.xyz/api/apikey=KUKIwrLK87gL6/kuki/moezilla/message={text}").json()
        aries = f"{Kuki['reply']}"
        if "Aries" in text or "aries" in text or "ARIES" in text:
            await bot.send_chat_action(chid, "typing")
        
        await message.reply_text(aries)
    
    except Exception as e:
        await bot.send_message(-1001545036829 , f"error in chatbot:\n\n{e}")

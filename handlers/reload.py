from asyncio import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message

from cache.admins import set
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from callsmusic import callsmusic
from callsmusic.queues import queues
from config import BOT_USERNAME
from cache.admins import admins
from handlers.play import cb_admin_check
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

@Client.on_message(filters.command("reload"))
async def update_admin(client, message: Message):
    chat_id = get_chat_id(message.chat)
    set(
        chat_id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_photo(
                photo=f"https://telegra.ph/file/ad4eca95908b25fafe7f2.jpg",
              caption=f"**✅ Reload Sukses __admin telah di update...__**",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Support", url=f"https://t.me/idzeroidsupport"),
                    InlineKeyboardButton("Owner", url=f"https://t.me/idzxartez")
                ]
            ]
        )
   )
    
# Copyright (C) 2021 VeezMusicProject


@Client.on_message(filters.command("cache"))
@errors
async def admincache(client, message: Message):
    set(
        message.chat.id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_photo(
                photo=f"https://telegra.ph/file/ad4eca95908b25fafe7f2.jpg",
              caption=f"**♻ Refresh Cache Sukses __admin cache di segarkan...__**",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Support", url=f"https://t.me/idzeroidsupport"),
                    InlineKeyboardButton("Owner", url=f"https://t.me/idzxartez"),
                ]
            ]
        )
   )

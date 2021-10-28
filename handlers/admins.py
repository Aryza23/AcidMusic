# Copyright by KennedyProject 2021
# https://github.com/KennedyProject/KennedyXMusic


from asyncio import QueueEmpty

from callsmusic import callsmusic
from callsmusic.queues import queues
from config import BOT_USERNAME, que
from cache.admins import admins
from handlers.play import cb_admin_check
from helpers.channelmusic import get_chat_id
from helpers.dbtools import delcmd_is_on, delcmd_off, delcmd_on, handle_user_status
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)


@Client.on_message(filters.text & ~filters.private)
async def delcmd(_, message: Message):
    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!") or message.text.startswith("."):
       await message.delete()
    await message.continue_propagation()

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

@Client.on_message(command(["pause", f"pause@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def pause(client, message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❌ **nothing is playing**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await client.send_message(message.chat.id, "▶️ **Music paused!**\n\n• To resume the music playback, use **command » /resume**")


@Client.on_message(command(["resume", f"resume@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def resume(client, message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❌ **Nothing is paused**")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await client.send_message(message.chat.id, "⏸ **Music resumed!**\n\n• To pause the music playback, use **command » /pause**")


@Client.on_message(command(["end", f"end@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def stop(client, message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❌ **nothing is playing**")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await client.send_message(message.chat.id, "✅ __The Userbot has disconnected from voice chat__")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(client, message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❌ **nothing is playing to skip**")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
            await client.send_message(message.chat.id, "__not enough queue, the assistant left the voice chat__")
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await client.send_message(message.chat.id, f"⏭️ __You've skipped to the next song__")


@Client.on_message(command(["auth", f"auth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("🔔 reply to message to authorize user !")
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "👮 user authorized.\n\nfrom now on, that's user can use the admin commands."
        )
    else:
        await message.reply("✅ user already authorized!")


@Client.on_message(command(["unauth", f"deauth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("🔔 reply to message to deauthorize user !")
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "👷 user deauthorized.\n\nfrom now that's user can't use the admin commands."
        )
    else:
        await message.reply("✅ user already deauthorized!")


# this is a anti cmd feature
@Client.on_message(command(["delcmd", f"delcmd@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "read the /help message to know how to use this command"
        )
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            return await message.reply_text("✅ already activated")
        await delcmd_on(chat_id)
        await message.reply_text("🟢 activated successfully")
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("🔴 disabled successfully")
    else:
        await message.reply_text(
            "read the /help message to know how to use this command"
        )

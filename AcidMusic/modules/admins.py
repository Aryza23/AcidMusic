from asyncio import QueueEmpty
from pyrogram import Client 
from pyrogram import filters
from pyrogram.types import Message

import sys
import os
import heroku3
import time
import traceback
import asyncio
import shutil
import psutil

from pyrogram.types import Dialog, Chat
from pyrogram.errors import UserAlreadyParticipant
from datetime import datetime
from functools import wraps
from os import environ, execle, path, remove
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from AcidMusic.config import UPSTREAM_REPO, U_BRANCH, HEROKU_URL, HEROKU_API_KEY, HEROKU_APP_NAME,

from AcidMusic.config import que
from AcidMusic.function.admins import set
from AcidMusic.helpers.channelmusic import get_chat_id
from AcidMusic.helpers.decorators import authorized_users_only
from AcidMusic.helpers.decorators import errors
from AcidMusic.helpers.filters import command
from AcidMusic.helpers.filters import other_filters
from AcidMusic.services.callsmusic import callsmusic
from AcidMusic.services.queues import queues


@Client.on_message(filters.command("adminreset"))
async def update_admin(client, message: Message):
    chat_id = get_chat_id(message.chat)
    set(
        chat_id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ Admin cache refreshed!")


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.active_chats) or (
        callsmusic.active_chats[chat_id] == "paused"
    ):
        await message.reply_text("❗ Nothing is playing!")
    else:
        callsmusic.pause(chat_id)
        await message.reply_text("▶️ Paused!")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.active_chats) or (
        callsmusic.active_chats[chat_id] == "playing"
    ):
        await message.reply_text("❗ Nothing is paused!")
    else:
        callsmusic.resume(chat_id)
        await message.reply_text("⏸ Resumed!")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.active_chats:
        await message.reply_text("❗ Nothing is streaming!")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        await callsmusic.stop(chat_id)
        await message.reply_text("❌ Stopped streaming!")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.active_chats:
        await message.reply_text("❗ Nothing is playing to skip!")
    else:
        queues.task_done(chat_id)
        if queues.is_empty(chat_id):
            await callsmusic.stop(chat_id)
        else:
            await callsmusic.set_stream(
                chat_id, 
                queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"- Skipped **{skip[0]}**\n- Now Playing **{qeue[0][0]}**")


@Client.on_message(filters.command("reload"))
@errors
async def admincache(client, message: Message):
    set(
        message.chat.id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ Admin cache refreshed!")


# Updator
REPO_ = UPSTREAM_REPO
BRANCH_ = U_BRANCH

@Client.on_message(filters.command("update") & filters.user(BOT_OWNER))
async def updatebot(_, message: Message):
    msg = await message.reply_text("`Updating Module is Starting! Please Wait...`")
    try:
        repo = Repo()
    except GitCommandError:
        return await msg.edit(
            "`Invalid Git Command!`"
        )
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "upstream" in repo.remotes:
            origin = repo.remote("upstream")
        else:
            origin = repo.create_remote("upstream", REPO_)
        origin.fetch()
        repo.create_head(U_BRANCH, origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    if repo.active_branch.name != U_BRANCH:
        return await msg.edit(
            f"Hmmm... Seems Like You Are Using Custom Branch Named `{repo.active_branch.name}`! Please Use `{U_BRANCH}` To Make This Works!"
        )
    try:
        repo.create_remote("upstream", REPO_)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(U_BRANCH)
    if not HEROKU_URL:
        try:
            ups_rem.pull(U_BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await run_cmd("pip3 install --no-cache-dir -r requirements.txt")
        await msg.edit("**Successfully Updated! Restarting Now!**")
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        exit()
        return
    else:
        await msg.edit("`Heroku Detected!`")
        await msg.edit("`Updating and Restarting has Started! Please wait for 5-10 Minutes!`")
        ups_rem.fetch(U_BRANCH)
        repo.git.reset("--hard", "FETCH_HEAD")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(HEROKU_URL)
        else:
            remote = repo.create_remote("heroku", HEROKU_URL)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except BaseException as error:
            await msg.edit(f"**Updater Error** \nTraceBack : `{error}`")
            return repo.__del__()


# Heroku Logs

async def edit_or_send_as_file(
    text: str,
    message: Message,
    client: Client,
    caption: str = "`Result!`",
    file_name: str = "result",
    parse_mode="md",
):
    """Send As File If Len Of Text Exceeds Tg Limit Else Edit Message"""
    if not text:
        await message.edit("`There is something other than text! Aborting...`")
        return
    if len(text) > 1024:
        await message.edit("`OutPut is Too Large to Send in TG, Sending As File!`")
        file_names = f"{file_name}.text"
        open(file_names, "w").write(text)
        await client.send_document(message.chat.id, file_names, caption=caption)
        await message.delete()
        if os.path.exists(file_names):
            os.remove(file_names)
        return
    else:
        return await message.edit(text, parse_mode=parse_mode)



heroku_client = None
if HEROKU_API_KEY:
    heroku_client = heroku3.from_key(HEROKU_API_KEY)

def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        heroku_app = None
        if not heroku_client:
            await message.reply_text(
                "`Please Add Heroku API Key To Use This Feature!`"
            )
        elif not HEROKU_APP_NAME:
            await edit_or_reply(
                message, "`Please Add Heroku APP Name To Use This Feature!`"
            )
        if HEROKU_APP_NAME and heroku_client:
            try:
                heroku_app = heroku_client.app(HEROKU_APP_NAME)
            except:
                await message.reply_text(
                    message, "`Heroku Api Key And App Name Doesn't Match! Check it again`"
                )
            if heroku_app:
                await func(client, message, heroku_app)

    return heroku_cli

@Client.on_message(filters.command("logs") & filters.user(BOT_OWNER))
@_check_heroku
async def logswen(client: Client, message: Message, happ):
    msg = await message.reply_text("`Please Wait For a Moment!`")
    logs = happ.get_log()
    capt = f"Heroku Logs Of `{HEROKU_APP_NAME}`"
    await edit_or_send_as_file(logs, msg, client, capt, "logs")


# Restart Your Bot
@Client.on_message(filters.command("restart") & filters.user(BOT_OWNER))
@_check_heroku
async def restart(client: Client, message: Message, hap):
    msg = await message.reply_text("`Restarting Now! Please wait...`")
    hap.restart()


# Set Heroku Var
@Client.on_message(filters.command("setvar") & filters.user(BOT_OWNER))
@_check_heroku
async def setvar(client: Client, message: Message, app_):
    msg = await message.reply_text(message, "`Please Wait...!`")
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg.edit("This is not the way bro! \n\n**Usage:**`/setvar VAR VALUE`")
        return
    if not " " in _var:
        await msg.edit("This is not the way bro! \n\n**Usage:**`/setvar VAR VALUE`")
        return
    var_ = _var.split(" ", 1)
    if len(var_) > 2:
        await msg.edit("This is not the way bro! \n\n**Usage:**`/setvar VAR VALUE`")
        return
    _varname, _varvalue = var_
    await msg.edit(f"**Variable:** `{_varname}` \n**New Value:** `{_varvalue}`")
    heroku_var[_varname] = _varvalue


# Delete Heroku Var
@Client.on_message(filters.command("delvar") & filters.user(BOT_OWNER))
@_check_heroku
async def delvar(client: Client, message: Message, app_):
    msg = await message.reply_text(message, "`Please Wait...!`")
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg.edit("`Give Me a Var Name To Delete!`")
        return
    if not _var in heroku_var:
        await msg.edit("`Lol! This Var Doesn't Even Exists!`")
        return
    await msg.edit(f"Sucessfully Deleted Var Named `{_var}`")
    del heroku_var[_var]

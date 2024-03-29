import datetime
import os

import discord
from discord.ext import tasks
from dotenv import load_dotenv
from pony.orm import db_session

from arcbot.command.core import *
from arcbot.command_parser.core import parse
from arcbot.log.core import get_logger
from arcbot.poll_manager.core import *
from arcbot.notification_manager.core import *
from arcbot.discord_model.core import Message

load_dotenv()

DISCORD_KEY = os.getenv('BOT_TOKEN')
PREFIX = '$'


def setup_client():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    if os.getenv('SHARDED'):
        return discord.AutoShardedClient(intents=intents)
    return discord.Client(intents=intents)


@db_session
def start_bot():
    client.run(DISCORD_KEY)


def get_client():
    return client


def wait_for_bot():
    while client.status != discord.Status.online:
        pass


client = setup_client()
logger = get_logger('arcBot-logger')


@client.event
async def on_ready():
    poll.start()
    poll_win.start()
    notifications.start()
    logger.info(f'We have logged in as {client.user}')


@client.event
async def on_typing(channel, user, when):
    pass


@client.event
async def on_disconnect():
    pass


@client.event
async def on_message_edit(before, after):
    pass


@client.event
async def on_message_delete(message):
    pass


@client.event
async def on_reaction_add(reaction, user):
    pass


@client.event
async def on_reaction_remove(reaction, user):
    pass


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


@tasks.loop(time=datetime.time(hour=14, minute=21))
async def poll():
    await send_poll_messages(client)


@tasks.loop(time=datetime.time(hour=14, minute=22))
async def poll_win():
    await notify_poll_winners(client)


# @tasks.loop(seconds=30)
@tasks.loop(minutes=1)
async def notifications():
    await send_notification_messages(client)


@client.event
async def on_message(message) -> Message | None:
    if message.author == client.user or not message.content.startswith(PREFIX):
        return

    command = parse(PREFIX, message.content)
    if command is None:
        logger.error(f'Invalid command: {message.content}')
        return

    logger.info(f'Executing command: {command.get_name()} with args {command.get_args()}')
    return await run(command.get_name(), command.get_args(),
                     DotDict({'message': message, 'client': client, 'channel': DiscordChannel(message.channel)}))

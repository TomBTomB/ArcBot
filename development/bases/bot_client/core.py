import os
import discord
from dotenv import load_dotenv

from development.components.audio_fetcher.core import fetch_audio_file
from development.components.bot_action.core import *
from development.components.command.core import *
from development.components.command_parser.core import parse
from development.components.log.core import get_logger

from development.components.queue_manager.core import add_song, get_queue_song_names, move_song, remove_song
from development.components.repository import core as repository

load_dotenv()

DISCORD_KEY = os.getenv('BOT_TOKEN')
PREFIX = '$'


def setup_client():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    if os.getenv('SHARDED'):
        return discord.AutoShardedClient(intents=intents)
    return discord.Client(intents=intents)


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


@client.event
async def on_message(message) -> Message | None:
    if message.author == client.user:
        return

    command = parse(PREFIX, message.content)
    if command is None:
        logger.error(f'Invalid command: {message.content}')
        return

    logger.info(f'Executing command: {command.get_name()} with args {command.get_args()}')
    return await run(command.get_name(), command.get_args(),
                     DotDict({'message': message, 'client': client, 'channel': DiscordChannel(message.channel)}))

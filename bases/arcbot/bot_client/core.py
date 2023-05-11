import os

import discord
from dotenv import load_dotenv

from components.arcbot.bot_action.core import send_message, Message
from components.arcbot.command.core import *
from components.arcbot.command_parser.core import parse
from components.arcbot.log.core import get_logger

logger = get_logger('arcBot-logger')

load_dotenv()

DISCORD_KEY = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
PREFIX = '$'


def start_bot():
    client.run(DISCORD_KEY)


def get_client():
    return client


def wait_for_bot():
    while client.status != discord.Status.online:
        pass


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


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


@client.event
async def on_message(message) -> Message | None:
    if message.author == client.user:
        return

    command = parse(PREFIX, message.content)
    if command is None:
        return
    logger.info(f'Command received: ' + command.get_name() + ' ' + str(command.get_args()))

    response, response_type = run(command.get_name(), command.get_args())

    match response_type:
        case 'MessageResponse':
            logger.info(f'Sending response: {response}')
            return await send_message(message.channel, response)

    # for channel in message.guild.channels:
    #     if channel.name == HISTORY_CHANNEL:
    #         await channel.send(f'Message from {message.author} in channel {message.channel}: {message.content} ')

    if message.content.startswith(f'{PREFIX}join'):
        if message.author.voice:
            channel = message.author.voice.channel
            await channel.connect()
            await message.channel.send('Bot joined')
        else:
            await message.channel.send('You must be in a voice channel first so I can join it.')

    elif message.content.startswith(f'{PREFIX}leave'):
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect()
            await message.channel.send('Bot left')
        else:
            await message.channel.send("I'm not in a voice channel, use the join command to make me join")

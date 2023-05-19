import os

import discord
from arcbot.bot_action.core import send_message, Message, join_or_leave, DiscordChannel, DiscordVoiceClient
from arcbot.command.core import *
from arcbot.command_parser.core import parse
from arcbot.log.core import get_logger
from dotenv import load_dotenv

load_dotenv()

DISCORD_KEY = os.getenv('BOT_TOKEN')
PREFIX = '$'


def setup_client():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
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
        case 'Message':
            logger.info(f'Sending response: {response}')
            return await send_message(DiscordChannel(message.channel), response)
        case 'Join/Leave':
            logger.info(f'Executing join/leave action: {response}')

            voice_channel = None if message.author.voice is None \
                else DiscordChannel(message.author.voice.channel)
            voice_client = None if message.guild.voice_client is None \
                else DiscordVoiceClient(message.guild.voice_client)

            reply = await join_or_leave(voice_channel, voice_client, should_join=response)

            logger.info(f'Sending response: {reply}')
            return await send_message(DiscordChannel(message.channel), reply)
        case 'Voice':
            logger.info(f'Sending voice response: {response}')

            if message.author.voice:
                channel = message.author.voice.channel
                # await join_channel(channel)
                # filename = fetch_audio_file(response)
                # await play_audio_file(filename)
                return await send_message(message.channel, 'Playing audio')
            else:
                return await send_message(message.channel, 'You must be in a voice channel first so I can join it.')
        case _:
            logger.error(f'Unimplemented command {command.get_name()}')

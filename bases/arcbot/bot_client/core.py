import os

import discord
from dotenv import load_dotenv

from arcbot.audio_fetcher.core import fetch_audio_file
from arcbot.bot_action.core import *
from arcbot.command.core import *
from arcbot.command_parser.core import parse
from arcbot.log.core import get_logger

from arcbot.queue_manager.core import *

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


@client.event
async def on_message(message) -> Message | None:
    if message.author == client.user:
        return

    command = parse(PREFIX, message.content)
    if command is None:
        return
    logger.info(f'Command received: ' + command.get_name() + ' ' + str(command.get_args()))

    response, response_type = run(command.get_name(), command.get_args())

    channel = DiscordChannel(message.channel)
    match response_type:
        case 'Message':
            logger.info(f'Sending response: {response}')
            return await send_message(channel, response)
        case 'Join/Leave':
            logger.info(f'Executing join/leave action: {response}')

            voice_channel, voice_client = get_voice_channel_and_client(message)

            reply = await join_or_leave(voice_channel, voice_client, should_join=response)

            logger.info(f'Sending response: {reply}')
            return await send_message(channel, reply)
        case 'Play':
            if os.name != 'nt' and not discord.opus.is_loaded():
                discord.opus.load_opus(os.getenv('OPUS_LIB'))

            logger.info(f'Executing voice action: {response}')

            voice_channel, voice_client = get_voice_channel_and_client(message)

            join_reply = await join_or_leave(voice_channel, voice_client, should_join=True)
            logger.info(f'Join/Leave result: {join_reply}')

            # Refresh voice client in case we just joined a channel
            _, voice_client = get_voice_channel_and_client(message)
            if voice_client is None:
                logger.info(f'Sending response: {join_reply}')
                return await send_message(channel, join_reply)

            file_name, url = await fetch_audio_file(response)
            logger.info(f'Fetched audio file: {file_name}')

            if voice_client.is_playing() or voice_client.is_paused():
                add_song(message.guild.id, file_name, url)
                return await send_message(channel, song_added_to_queue_message(file_name))

            reply = play_audio_file(file_name, url, voice_client,
                                    lambda: play_next_song(channel, voice_client, message.guild.id, client.loop))
            logger.info(f'Sending response: {reply}')
            return await send_message(channel, reply)
        case 'Pause/Resume':
            logger.info(f'Executing pause/resume action: {response}')
            _, voice_client = get_voice_channel_and_client(message)
            if voice_client is None:
                return await send_message(channel, Strings.Action.bot_not_connected)
            pause_or_resume(voice_client)
            return await send_message(channel, response)
        case 'Queue':
            logger.info(f'Executing queue action: {response}')
            songs: list[str] = get_queue_song_names(message.guild.id)
            if len(songs) == 0:
                return await send_message(channel, Strings.Queue.empty)
            return await send_message(channel, '\n'.join([f'{i + 1}. {song}' for i, song in enumerate(songs)]))
        case 'Skip':
            logger.info(f'Executing skip action: {response}')
            _, voice_client = get_voice_channel_and_client(message)
            if voice_client is None:
                return await send_message(channel, Strings.Action.bot_not_connected)
            new_song = skip_song(message.guild.id, voice_client, channel, client.loop)
            if new_song is None:
                await leave_channel(voice_client)
                return await send_message(channel, Strings.Action.bot_disconnected)
            return await send_message(channel, Strings.Action.now_playing(new_song))
        case 'Move':
            logger.info(f'Executing move action: {response}')
            move_from, move_to = response.split(' ')
            moved_song = move_song(message.guild.id, int(move_from) - 1, int(move_to) - 1)
            if moved_song is None:
                return await send_message(channel, Strings.Error.invalid_move)
            return await send_message(channel, Strings.Action.song_moved(moved_song, move_to))
        case 'Remove':
            logger.info(f'Executing remove action: {response}')
            removed_song = remove_song(message.guild.id, int(response) - 1)
            if removed_song is None:
                return await send_message(channel, Strings.Error.invalid_remove)
            return await send_message(channel, Strings.Action.song_removed(removed_song))
        case _:
            logger.error(f'Unimplemented command {command.get_name()}')


def get_voice_channel_and_client(message):
    voice_channel = None if message.author.voice is None \
        else DiscordChannel(message.author.voice.channel)
    voice_client = None if message.guild.voice_client is None \
        else DiscordVoiceClient(message.guild.voice_client)
    return voice_channel, voice_client

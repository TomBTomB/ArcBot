import importlib
import os

from dotenv import load_dotenv

from arcbot.discord_model.core import *
from arcbot.log.core import get_logger
from arcbot.queue_manager.core import get_next_song

from arcbot.strings.core import Strings

load_dotenv()
logger = get_logger('arcBot-logger')
send_message = importlib.import_module(os.getenv('SEND_MESSAGE_MODULE')).send_message


async def join_or_leave(channel: Channel, voice_client: VoiceClient, should_join: bool):
    if not channel:
        return Strings.Action.user_not_connected

    if voice_client is None:
        if should_join:
            await channel.connect()
            return Strings.Action.bot_connected
        else:
            return Strings.Action.bot_not_connected

    if voice_client.get_channel() == channel:
        if should_join:
            return Strings.Action.bot_already_connected
        else:
            await voice_client.disconnect()
            return Strings.Action.bot_disconnected
    else:
        if should_join:
            await voice_client.disconnect()
            await channel.connect()
            return Strings.Action.bot_moved
        else:
            return Strings.Action.bot_not_connected


def play_audio_file(file_name: str, url: str, voice_client: VoiceClient, after: callable) -> str:
    voice_client.play(url, after)
    return Strings.Action.now_playing(file_name)


def song_added_to_queue_message(file_name: str) -> str:
    return Strings.Action.song_added_to_queue(file_name)


def play_next_song(channel: Channel, voice_client: VoiceClient, guild_id: int, loop: asyncio.AbstractEventLoop):
    file_name, url = get_next_song(guild_id)
    if file_name is None:
        asyncio.run_coroutine_threadsafe(leave_channel(voice_client), loop)
        return
    message = play_audio_file(file_name, url, voice_client,
                              lambda: play_next_song(channel, voice_client, guild_id, loop))
    asyncio.run_coroutine_threadsafe(send_message(channel, message), loop)


def pause_or_resume(voice_client: VoiceClient):
    if voice_client.is_playing():
        voice_client.pause()
    else:
        voice_client.resume()


def resume_playing(voice_client: VoiceClient):
    voice_client.resume()


async def leave_channel(voice_client: VoiceClient):
    await voice_client.disconnect()


def pause_playing(voice_client: VoiceClient):
    voice_client.pause()


def skip_song(guild_id: int, voice_client: VoiceClient, channel: Channel,
              loop: asyncio.AbstractEventLoop) -> str | None:
    pause_playing(voice_client)
    next_song = get_next_song(guild_id)
    if next_song[0] is None:
        return None
    else:
        play_audio_file(next_song[0], next_song[1], voice_client,
                        lambda: play_next_song(channel, voice_client, guild_id, loop))
        return next_song[0]


async def add_reactions(message: Message, reactions):
    for reaction in reactions:
        await message.add_reaction(reaction)

import asyncio

import discord

from development.components.log.core import get_logger
from development.components.queue_manager.core import get_next_song

from development.components.strings.core import Strings

logger = get_logger('arcBot-logger')


class Message:
    def get_content(self) -> str:
        pass


class DiscordMessage(Message):
    def __init__(self, discord_message: discord.Message):
        self.__discord_message = discord_message

    def get_content(self) -> str:
        return self.__discord_message.content


class MockMessage(Message):
    def __init__(self, content: str):
        self.__content = content

    def get_content(self) -> str:
        return self.__content


class Channel:
    async def send(self, message: str) -> Message:
        pass

    async def connect(self):
        pass


class DiscordChannel(Channel):

    def __init__(self, discord_channel: discord.TextChannel | discord.VoiceChannel | discord.StageChannel):
        self.__discord_channel = discord_channel

    def __eq__(self, o: object) -> bool:
        if isinstance(o, DiscordChannel):
            return self.__discord_channel == o.__discord_channel
        return False

    async def send(self, message: str) -> Message:
        return DiscordMessage(discord_message=await self.__discord_channel.send(message))

    async def connect(self):
        await self.__discord_channel.connect()

    async def disconnect(self):
        a = await self.__discord_channel.connect()
        await a.disconnect()


class MockChannel(Channel):

    async def send(self, message: str) -> Message:
        return MockMessage(content=message)

    async def connect(self):
        pass


class VoiceClient:

    async def disconnect(self):
        pass

    def get_channel(self) -> Channel:
        pass

    def play(self, url: str, after: asyncio.AbstractEventLoop) -> None:
        pass

    def is_playing(self) -> bool:
        pass

    def stop(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def is_paused(self) -> bool:
        pass


class DiscordVoiceClient(VoiceClient):
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    def __init__(self, discord_voice_client: discord.VoiceClient):
        self.__discord_voice_client = discord_voice_client

    async def disconnect(self):
        await self.__discord_voice_client.disconnect()

    def get_channel(self) -> Channel:
        return DiscordChannel(self.__discord_voice_client.channel)

    def play(self, url: str, after: callable):
        audio_source = discord.FFmpegPCMAudio(url, **self.ffmpeg_options)
        self.__discord_voice_client.play(audio_source,
                                         after=lambda _: after())

    def is_playing(self) -> bool:
        return self.__discord_voice_client.is_playing()

    def pause(self):
        self.__discord_voice_client.pause()

    def resume(self):
        self.__discord_voice_client.resume()

    def stop(self):
        self.__discord_voice_client.stop()

    def is_paused(self) -> bool:
        return self.__discord_voice_client.is_paused()


class MockVoiceClient(VoiceClient):

    async def disconnect(self):
        return "Disconnected"

    def get_channel(self) -> Channel:
        return MockChannel()

    def play(self, *_) -> None:
        pass

    def is_playing(self) -> bool:
        pass

    def stop(self):
        pass


async def send_message(channel: Channel, message: str) -> Message:
    """Send a message to a channel.
    :param channel: the channel to send the message to
    :param message: the message to send
    :raises ValueError: if the message is empty or None
    """
    message_stripped = message.strip()
    if len(message_stripped) == 0:
        raise ValueError('Message cannot be empty')
    logger.info(f'Sending message: {message_stripped}')
    return await channel.send(message_stripped)


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

import asyncio

import discord


class Message:
    def __init__(self, message: dict):
        self.__content = message['content']
        self.__id = message['id']

    def get_content(self) -> str:
        return self.__content

    def get_id(self) -> int:
        return self.__id

    async def add_reaction(self, reaction):
        pass


class DiscordMessage(Message):
    def __init__(self, discord_message: discord.Message):
        self.__discord_message = discord_message

    def get_content(self) -> str:
        return self.__discord_message.content

    def get_id(self) -> int:
        return self.__discord_message.id

    async def add_reaction(self, reaction):
        await self.__discord_message.add_reaction(reaction)


class MockMessage(Message):
    def __init__(self, content: str):
        self.__content = content

    def get_content(self) -> str:
        return self.__content

    def get_id(self) -> int:
        return 0

    async def add_reaction(self, reaction):
        pass


class Channel:
    async def send(self, message: str) -> Message:
        pass

    async def connect(self):
        pass

    def get_id(self):
        pass

    def get_guild_id(self):
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

    def get_id(self):
        return self.__discord_channel.id

    def get_guild_id(self):
        return self.__discord_channel.guild.id


class MockChannel(Channel):

    async def send(self, message: str) -> Message:
        return MockMessage(content=message)

    async def connect(self):
        pass

    def get_id(self):
        return 0

    def get_guild_id(self):
        return 0


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

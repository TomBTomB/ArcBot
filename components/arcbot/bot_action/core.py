import discord


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

    def play(self, url: str) -> None:
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

    def play(self, url: str):
        audio_source = discord.FFmpegPCMAudio(url, **self.ffmpeg_options)
        self.__discord_voice_client.play(audio_source)


class MockVoiceClient(VoiceClient):

    async def disconnect(self):
        return "Disconnected"

    def get_channel(self) -> Channel:
        return MockChannel()

    def play(self, _) -> None:
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
    return await channel.send(message_stripped)


async def join_or_leave(channel: Channel, voice_client: VoiceClient, should_join: bool):
    if not channel:
        return 'It seems your are in the void.'

    if voice_client is None:
        if should_join:
            await channel.connect()
            return 'Who disturbs my slumber?'
        else:
            return 'I am not amongst you.'

    if voice_client.get_channel() == channel:
        if should_join:
            return 'I am already amongst you.'
        else:
            await voice_client.disconnect()
            return 'I have returned to the void from whence I came.'
    else:
        if should_join:
            await voice_client.disconnect()
            await channel.connect()
            return 'Whomst has summoned the almighty one?'
        else:
            return 'I am not amongst you.'


def play_audio_file(file_name: str, url: str, voice_client: VoiceClient) -> str:
    voice_client.play(url)
    return f'Now playing: {file_name}'

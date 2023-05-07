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


class DiscordChannel(Channel):

    def __init__(self, discord_channel: discord.DMChannel):
        self.__discord_channel = discord_channel

    async def send(self, message: str) -> Message:
        return DiscordMessage(discord_message=await self.__discord_channel.send(message))


class MockChannel(Channel):

    async def send(self, message: str) -> Message:
        return MockMessage(content=message)


async def send_message(channel: Channel, message: str) -> Message:
    """Send a message to a channel.
    :param channel: the channel to send the message to
    :param message: the message to send
    :raises ValueError: if the message is empty or None
    """
    message_stripped = message.strip()
    if len(message_stripped) == 0:
        raise ValueError("Message cannot be empty")
    return await channel.send(message_stripped)

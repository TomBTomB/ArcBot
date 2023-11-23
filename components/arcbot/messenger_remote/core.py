from arcbot.bot_action.core import Channel, Message
from arcbot.log.core import get_logger
import requests

base_url = 'http://localhost:5001/message'
logger = get_logger('arcBot-logger')


async def send_message(channel: Channel, message: str) -> Message:
    """Send a message to a channel.
    :param channel: the channel to send the message to
    :param message: the message to send
    :raises ValueError: if the message is empty or None
    """
    response = requests.post(f'{base_url}/{channel.get_guild_id()}/{channel.get_id()}'
                             , json={'message': message})
    if response.status_code != 200:
        logger.error(f'Failed to send message: {message}')
    return Message(response.json())

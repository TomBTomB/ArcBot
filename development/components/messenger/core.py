from development.components.discord_model.core import *
from development.components.log.core import get_logger

logger = get_logger('arcBot-logger')


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

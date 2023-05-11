import unittest

from components.arcbot.bot_action import core as bot_action
from components.arcbot.bot_action.core import MockChannel


class TestBotAction(unittest.IsolatedAsyncioTestCase):
    async def test_send_message(self):
        message_content = 'Hello World!'
        sent_message = await bot_action.send_message(MockChannel(), message_content)
        self.assertIsNotNone(sent_message)
        self.assertEqual(message_content, sent_message.get_content())

    async def test_send_empty_message(self):
        message_content = ''
        with self.assertRaises(ValueError):
            await bot_action.send_message(MockChannel(), message_content)

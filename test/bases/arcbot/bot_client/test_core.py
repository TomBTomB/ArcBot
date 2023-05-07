import multiprocessing
import unittest

from bases.arcbot.bot_client import core as bot_client
from components.arcbot.bot_action.core import MockChannel


class Message:
    def __init__(self, content):
        self.content = content
        self.author = "test"
        self.channel = MockChannel()


class TestCore(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.thread = multiprocessing.Process(target=bot_client.start_bot)
        self.thread.start()

    async def asyncTearDown(self) -> None:
        self.thread.terminate()

    async def test_ping(self):
        bot_client.wait_for_bot()

        result = await bot_client.on_message(Message("$ping"))
        self.assertIsNotNone(result)
        self.assertEqual("Pong!", result.get_content())

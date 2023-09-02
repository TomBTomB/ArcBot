import unittest

import discord
from arcbot.bot_action import core as bot_action
from arcbot.bot_action.core import MockChannel, MockMessage, MockVoiceClient


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

    async def test_join_no_voice_client(self):
        # test joining a mock channel with no voice client
        channel = MockChannel()
        voice_client = None
        should_join = True
        result = await bot_action.join_or_leave(channel, voice_client, should_join)
        self.assertEqual(result, "Who disturbs my slumber?")  # check if the result is the expected response

    async def test_leave_no_voice_client(self):
        # test leaving a mock channel with no voice client
        channel = MockChannel()
        voice_client = MockVoiceClient()
        should_join = False
        result = await bot_action.join_or_leave(channel, voice_client, should_join)
        self.assertEqual(result, "I am not amongst you.")  # check if the result is the expected response

    async def test_join_voice_client(self):
        # test joining a mock channel with a mock voice client in the same channel
        channel = MockChannel()
        voice_client = MockVoiceClient()
        should_join = True
        result = await bot_action.join_or_leave(channel, voice_client, should_join)
        self.assertEqual(result, "I am already amongst you.")  # check if the result is the expected response

    def test_play_audio_file(self):
        # test playing an audio file with a mock voice client
        file_name = "Never Gonna Give You Up"
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        voice_client = MockVoiceClient()
        result = bot_action.play_audio_file(file_name, url, voice_client)
        self.assertEqual(result, f"Now playing: {file_name}")  # check if the result is the expected response

    async def test_send_message_with_newline(self):
        # test sending a message with a newline character to a mock channel
        message_content = "Hello\nWorld!"
        sent_message = await bot_action.send_message(MockChannel(), message_content)
        self.assertIsNotNone(sent_message)
        self.assertEqual(message_content, sent_message.get_content())

    async def test_send_message_with_whitespace(self):
        # test sending a message with only whitespace characters to a mock channel
        message_content = "   "
        with self.assertRaises(ValueError):
            await bot_action.send_message(MockChannel(), message_content)

    async def test_join_no_channel(self):
        # test joining with no channel and no voice client
        channel = None
        voice_client = None
        should_join = True
        result = await bot_action.join_or_leave(channel, voice_client, should_join)
        self.assertEqual(result, "It seems your are in the void.")  # check if the result is the expected response

    async def test_leave_voice_client_in_different_channel(self):
        # test leaving a mock channel with a mock voice client in a different channel
        channel = MockChannel()
        voice_client = MockVoiceClient()
        voice_client.channel = MockChannel()  # set the voice client's channel to a different mock channel
        should_join = False
        result = await bot_action.join_or_leave(channel, voice_client, should_join)
        self.assertEqual(result, "I am not amongst you.")  # check if the result is the expected response

    async def test_join_voice_client_in_different_channel(self):
        # test joining a mock channel with a mock voice client in a different channel
        channel = MockChannel()
        voice_client = MockVoiceClient()
        voice_client.channel = MockChannel()  # set the voice client's channel to a different mock channel
        should_join = True
        result = await bot_action.join_or_leave(channel, voice_client, should_join)
        self.assertEqual(result,
                         "Whomst has summoned the almighty one?")  # check if the result is the expected response

    def test_play_audio_file_with_invalid_url(self):
        # test playing an audio file with an invalid URL and a mock voice client
        file_name = "Never Gonna Give You Up"
        url = "https://www.example.com"
        voice_client = MockVoiceClient()
        with self.assertRaises(discord.FFmpegError):  # expect an exception to be raised
            bot_action.play_audio_file(file_name, url, voice_client)

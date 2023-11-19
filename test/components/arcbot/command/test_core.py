import unittest

from arcbot.command import core as command

from bases.arcbot.bot_client.core import DotDict
from components.arcbot.bot_action.core import MockChannel, MockVoiceClient


class TestCore(unittest.TestCase):
    async def test_run_help(self):
        # test running the help command with no arguments
        name = "help"
        args = ""
        result, response_type = await command.run(name, args, DotDict({'message': "", 'client': MockVoiceClient(), 'channel': MockChannel()}))
        self.assertEqual(response_type, "Message")  # check if the response type is correct
        self.assertEqual(result, '\n'.join(
            [str(command_value) for command_value in
             command.commands.values()]))  # check if the result is the expected output

    async def test_run_ping(self):
        # test running the ping command with no arguments
        name = "ping"
        args = ""
        result, response_type = await command.run(name, args, DotDict({'message': "", 'client': MockVoiceClient(), 'channel': MockChannel()}))
        self.assertEqual(response_type, "Message")  # check if the response type is correct
        self.assertEqual(result, "Pong!")  # check if the result is the expected output

    async def test_run_join(self):
        # test running the join command with no arguments
        name = "join"
        args = ""
        result, response_type = await command.run(name, args, DotDict({'message': "", 'client': MockVoiceClient(), 'channel': MockChannel()}))
        self.assertEqual(response_type, "Join/Leave")  # check if the response type is correct
        self.assertTrue(result)  # check if the result is True

    async def test_run_leave(self):
        # test running the leave command with no arguments
        name = "leave"
        args = ""
        result, response_type = await command.run(name, args, DotDict({'message': "", 'client': MockVoiceClient(), 'channel': MockChannel()}))
        self.assertEqual(response_type, "Join/Leave")  # check if the response type is correct
        self.assertFalse(result)  # check if the result is False

    async def test_run_play(self):
        # test running the play command with a valid URL argument
        name = "play"
        args = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result, response_type = await command.run(name, args, DotDict({'message': "", 'client': MockVoiceClient(), 'channel': MockChannel()}))
        self.assertEqual(response_type, "Play")  # check if the response type is correct
        self.assertEqual(result, args)  # check if the result is the same as the argument

    async def test_run_ping_with_argument(self):
        # test running the ping command with an argument
        name = "ping"
        args = "foo"
        result, response_type = await command.run(name, args, DotDict({'message': "", 'client': MockVoiceClient(), 'channel': MockChannel()}))
        self.assertEqual(response_type, "Message")  # check if the response type is correct
        self.assertEqual(result, "Pong!")  # check if the result is the expected output

    async def test_run_join_with_argument(self):
        # test running the join command with an argument
        name = "join"
        args = "foo"
        result, response_type = await command.run(name, args, DotDict({'message': "", 'client': MockVoiceClient(), 'channel': MockChannel()}))
        self.assertEqual(response_type, "Join/Leave")  # check if the response type is correct
        self.assertTrue(result)  # check if the result is True

    async def test_run_leave_with_argument(self):
        # test running the leave command with an argument
        name = "leave"
        args = "foo"
        result, response_type = await command.run(name, args, DotDict({'message': "", 'client': MockVoiceClient(), 'channel': MockChannel()}))
        self.assertEqual(response_type, "Join/Leave")  # check if the response type is correct
        self.assertFalse(result)  # check if the result is False


if __name__ == '__main__':
    unittest.main()

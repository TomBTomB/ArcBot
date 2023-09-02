import unittest

from arcbot.command import core as command


class TestCore(unittest.TestCase):
    def test_run_help(self):
        # test running the help command with no arguments
        name = "help"
        args = ""
        result, response_type = command.run(name, args)
        self.assertEqual(response_type, "Message")  # check if the response type is correct
        self.assertEqual(result, '\n'.join(
            [str(command_value) for command_value in
             command.commands.values()]))  # check if the result is the expected output

    def test_run_ping(self):
        # test running the ping command with no arguments
        name = "ping"
        args = ""
        result, response_type = command.run(name, args)
        self.assertEqual(response_type, "Message")  # check if the response type is correct
        self.assertEqual(result, "Pong!")  # check if the result is the expected output

    def test_run_join(self):
        # test running the join command with no arguments
        name = "join"
        args = ""
        result, response_type = command.run(name, args)
        self.assertEqual(response_type, "Join/Leave")  # check if the response type is correct
        self.assertTrue(result)  # check if the result is True

    def test_run_leave(self):
        # test running the leave command with no arguments
        name = "leave"
        args = ""
        result, response_type = command.run(name, args)
        self.assertEqual(response_type, "Join/Leave")  # check if the response type is correct
        self.assertFalse(result)  # check if the result is False

    def test_run_play(self):
        # test running the play command with a valid URL argument
        name = "play"
        args = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result, response_type = command.run(name, args)
        self.assertEqual(response_type, "Voice")  # check if the response type is correct
        self.assertEqual(result, args)  # check if the result is the same as the argument

    def test_run_help_with_argument(self):
        # test running the help command with an argument
        name = "help"
        args = "ping"
        result, response_type = command.run(name, args)
        self.assertEqual(response_type, "Message")  # check if the response type is correct
        self.assertEqual(result, "ping: Pings the bot.")  # check if the result is the expected output

    def test_run_ping_with_argument(self):
        # test running the ping command with an argument
        name = "ping"
        args = "foo"
        result, response_type = command.run(name, args)
        self.assertEqual(response_type, "Message")  # check if the response type is correct
        self.assertEqual(result, "Pong!")  # check if the result is the expected output

    def test_run_join_with_argument(self):
        # test running the join command with an argument
        name = "join"
        args = "foo"
        result, response_type = command.run(name, args)
        self.assertEqual(response_type, "Join/Leave")  # check if the response type is correct
        self.assertTrue(result)  # check if the result is True

    def test_run_leave_with_argument(self):
        # test running the leave command with an argument
        name = "leave"
        args = "foo"
        result, response_type = command.run(name, args)
        self.assertEqual(response_type, "Join/Leave")  # check if the response type is correct
        self.assertFalse(result)  # check if the result is False

    def test_run_play_with_invalid_url(self):
        # test running the play command with an invalid URL argument
        name = "play"
        args = "https://www.example.com"
        result, response_type = command.run(name, args)
        self.assertEqual(response_type, "Voice")  # check if the response type is correct
        self.assertIsNone(result)  # check if the result is None


if __name__ == '__main__':
    unittest.main()

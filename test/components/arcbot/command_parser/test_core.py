import unittest

from components.arcbot.command_parser import core as command_parser


class TestCommandParser(unittest.TestCase):
    def test_parse(self):
        command = command_parser.parse('!', '!test arg1 arg2')
        self.assertIsNotNone(command)
        self.assertEqual('test', command.get_name())
        self.assertEqual('arg1 arg2', command.get_args())

    def test_parse_no_prefix(self):
        command = command_parser.parse('!', 'test arg1 arg2')
        self.assertIsNone(command)

    def test_parse_no_args(self):
        command = command_parser.parse('!', '!test')
        self.assertIsNotNone(command)
        self.assertEqual('test', command.get_name())
        self.assertIsNone(command.get_args())

    def test_parse_no_command(self):
        command = command_parser.parse('!', '!')
        self.assertIsNone(command)

    def test_parse_no_args_with_space(self):
        command = command_parser.parse('!', '!test ')
        self.assertIsNotNone(command)
        self.assertEqual('test', command.get_name())
        self.assertIsNone(command.get_args())

    def test_parse_no_args_with_space_and_prefix(self):
        command = command_parser.parse('!', ' !test')
        self.assertIsNotNone(command)
        self.assertEqual('test', command.get_name())
        self.assertIsNone(command.get_args())

    def test_parse_invalid_prefix(self):
        with self.assertRaises(ValueError):
            command_parser.parse('!!', '!test arg1 arg2')
        with self.assertRaises(ValueError):
            command_parser.parse('', '!test arg1 arg2')

    def test_parse_empty(self):
        command = command_parser.parse('!', '')
        self.assertIsNone(command)

    def test_parse_args_no_name(self):
        command = command_parser.parse('!', '! arg1 arg2')
        self.assertIsNone(command)


if __name__ == '__main__':
    unittest.main()

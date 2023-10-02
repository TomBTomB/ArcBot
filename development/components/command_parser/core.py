class ParsedCommand:
    def __init__(self, name: str, args: str | None):
        self.__name = name
        self.__args = args

    def get_name(self) -> str:
        return self.__name

    def get_args(self) -> str | None:
        return self.__args


def parse(prefix: str, message: str) -> ParsedCommand | None:
    """Parse a message into a command.
            :param prefix: the command prefix, limited to one character
            :param message: the full message to parse
            :return: the parsed command, or None if the message is not a valid command
            :raises ValueError: if the prefix is not one character long
            """
    if len(prefix.strip()) != 1:
        raise ValueError('prefix must be one character long')

    message_stripped = message.strip()

    if not message_stripped.startswith(prefix) or len(message_stripped) == len(prefix):
        return None

    message_no_prefix = message_stripped[len(prefix):]
    if ' ' not in message_no_prefix:
        return ParsedCommand(message_no_prefix, None)

    name = message_no_prefix[:message_no_prefix.find(' ')]
    if name == '':
        return None

    args = message_no_prefix[message_no_prefix.find(' ') + 1:]
    return ParsedCommand(name, args)

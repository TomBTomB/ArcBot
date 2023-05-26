def help_command(_args) -> str:
    return '\n'.join([str(command) for command in commands.values()])


def ping(_args) -> str:
    return 'Pong!'


def join(_args) -> bool:
    return True


def leave(_args) -> bool:
    return False


def play(args) -> str:
    return args


class Command:
    def __init__(self, name: str, description: str, function: callable, response_type: str):
        self.__name = name
        self.__description = description
        self.__function = function
        self.__response_type = response_type

    def __str__(self):
        return f'{self.__name}: {self.__description}'

    def get_response_type(self):
        return self.__response_type

    def function(self, args):
        return self.__function(args)


commands = {
    'help': Command(name='help', description='Shows every possible command.', function=help_command,
                    response_type='Message'),
    'ping': Command(name='ping', description="Pings the bot.", function=ping,
                    response_type="Message"),
    'join': Command(name='join', description="Joins the voice channel you are in.", function=join,
                    response_type="Join/Leave"),
    'leave': Command(name='leave', description="Leaves the voice channel you are in.", function=leave,
                     response_type="Join/Leave"),
    'play': Command(name='play', description="Plays the requested song. (from an url)", function=play,
                    response_type="Voice"),
}


def run(name, args) -> (str | bool, str):
    command = commands[name]
    return command.function(args), command.get_response_type()

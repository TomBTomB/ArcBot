from arcbot.strings.core import Strings


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


def pause(_args) -> str:
    return 'Paused song.'


def resume(_args) -> str:
    return 'Resuming...'


def skip(_args) -> str:
    return 'Skipped song.'


def queue(_args) -> None:
    return None


def move(args) -> str:
    return args


def remove(args) -> str:
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
    'help': Command(name='help', description=Strings.Description.help, function=help_command,
                    response_type='Message'),
    'ping': Command(name='ping', description=Strings.Description.ping, function=ping,
                    response_type="Message"),
    'join': Command(name='join', description=Strings.Description.join, function=join,
                    response_type="Join/Leave"),
    'leave': Command(name='leave', description=Strings.Description.leave, function=leave,
                     response_type="Join/Leave"),
    'play': Command(name='play', description=Strings.Description.play, function=play,
                    response_type="Play"),
    'pause': Command(name='pause', description=Strings.Description.pause, function=pause,
                     response_type="Pause/Resume"),
    'resume': Command(name='resume', description=Strings.Description.resume, function=resume,
                      response_type="Pause/Resume"),
    'stop': Command(name='stop', description=Strings.Description.stop, function=leave,
                    response_type="Join/Leave"),
    'skip': Command(name='skip', description=Strings.Description.skip, function=skip,
                    response_type="Skip"),
    'queue': Command(name='queue', description=Strings.Description.queue, function=queue,
                     response_type="Queue"),
    'move': Command(name='move', description=Strings.Description.move, function=move,
                    response_type="Move"),
    'remove': Command(name='remove', description=Strings.Description.remove, function=remove,
                      response_type="Remove")
}


def run(name, args) -> (str | bool, str):
    command = commands[name]
    return command.function(args), command.get_response_type()

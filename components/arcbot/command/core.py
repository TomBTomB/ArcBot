def help_command(_args) -> str:
    return '\n'.join([str(command) for command in commands.values()])


def ping(_args) -> str:
    return 'Pong!'


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
    'help': Command(name='Help', description='Shows every possible command.', function=help_command,
                    response_type='MessageResponse'),
    'ping': Command(name='Ping', description="Pings the bot.", function=ping,
                    response_type="MessageResponse"),
}


def run(name, args) -> (str, str):
    command = commands[name]
    return command.function(args), command.get_response_type()

class Command:
    def __init__(self, name: str, args: str | None):
        self.__name = name
        self.__args = args

    def get_name(self) -> str:
        return self.__name

    def get_args(self) -> str:
        return self.__args


def help_command(_args) -> str:
    return "Hello World!"  # TODO implement


def ping(_args) -> str:
    return "Pong!"

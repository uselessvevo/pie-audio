import colorama
from datetime import datetime


colorama.init()


class LoggingEnum:
    INFO = colorama.Style.NORMAL
    WARNING = colorama.Fore.LIGHTMAGENTA_EX
    CRITICAL = colorama.Fore.LIGHTRED_EX


class DummyLogger:

    def __init__(self, name: str):
        self._name = name
        self._format = f'[{datetime.now()} | {name}]'

    def log(self, message: str, log_level: LoggingEnum = LoggingEnum.INFO):
        print(f'{log_level}{self._format} {"":<3} {message}{colorama.Style.RESET_ALL}')

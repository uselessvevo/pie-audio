import os.path
from pathlib import Path

import colorama
from datetime import datetime


colorama.init()


class LoggingEnum:
    INFO = colorama.Style.NORMAL
    WARNING = colorama.Fore.LIGHTMAGENTA_EX
    CRITICAL = colorama.Fore.LIGHTRED_EX


class DummyLogger:

    def __init__(self, name: str, root: str = 'logs') -> None:
        self._name = name
        self._format = f'[{datetime.now()} | {name}]'
        self._file = f'{root}/logs_{datetime.now().date()}.log'

    def log(self, message: str, log_level: LoggingEnum = LoggingEnum.INFO):
        message = f'{log_level}{self._format} {"":<3} {message}{colorama.Style.RESET_ALL}'
        print(message)
        with open(self._file, 'a') as file:
            file.writelines(f'{message}\n')

    def info(self, message):
        self.log(message)

    def warn(self, message):
        self.log(message, LoggingEnum.WARNING)

    def critical(self, message):
        self.log(message, LoggingEnum.CRITICAL)

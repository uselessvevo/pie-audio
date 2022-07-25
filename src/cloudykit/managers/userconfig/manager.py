import os.path
from pathlib import Path
from typing import Any

from dotty_dict import Dotty

from cloudykit.abstracts.manager import IManager
from cloudykit.utils.files import read_json, write_json
from cloudykit.observers.filesystem import FileSystemObserver
from cloudykit.utils.logger import DummyLogger
from cloudykit.managers.system.manager import System


logger = DummyLogger('UserConfigManager')


class UserConfigManager(IManager):
    name = 'userconfig'

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._dictionary: Dotty = Dotty({})
        self._observer = FileSystemObserver()
        self._user_folder = Path(os.path.expanduser('~'), '.crabs')
        logger.info(f'User folder is "{self._user_folder}"')

    def restore_crabs(self):
        if not self._user_folder.exists():
            self._user_folder.mkdir()

        if self._user_folder.exists():
            files = tuple(map(self._user_folder.joinpath, System.config.get('cloudykit.userconfig').keys()))
            files_dict = System.config.get('cloudykit.userconfig')
            for file in files:
                write_json(str(file), files_dict.get(file.name))

    def mount(self) -> None:
        for config in self._user_folder.rglob('*.json'):
            if not self._dictionary.get(config.name):
                self._dictionary[config.stem] = {}
            self._dictionary[config.stem].update(**read_json(str(config)))

        self._observer.add_handler(str(self._user_folder), str(self._user_folder))

    def unmount(self, *args, **kwargs) -> None:
        self._dictionary = Dotty({})
        self._observer.remove_handler(str(self._user_folder))

    def set(self, key, data: Any) -> None:
        self._dictionary[key] = data

    def get(self, key, default: Any = None) -> Any:
        return self._dictionary.get(key, default)

    def save(self, section: str, data: dict) -> None:
        if not self._dictionary.get(section):
            raise FileNotFoundError(f'File "{section}" not found')

        write_json(str(self._user_folder / f'{section}.json'), data)
        self._dictionary[section] = data

    @property
    def root(self):
        return self._user_folder

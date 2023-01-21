from pathlib import Path
from typing import Any
from dotty_dict import Dotty
from functools import lru_cache

from cloudykit.system.manager import System
from cloudykit.objects.manager import BaseManager
from cloudykit.utils.files import read_json, write_json
from cloudykit.observers.filesystem import FileSystemObserver


class UserConfigsManager(BaseManager):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._dictionary: Dotty = Dotty({})
        self._observer = FileSystemObserver()
        self._user_folder = Path(System.config.USER_CONFIGS_FOLDER_NAME)
        self._logger.info(f'User folder set to "{self._user_folder}"')

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

    @lru_cache
    def get(self, key, default: Any = None) -> Any:
        return self._dictionary.get(key, default)

    def save(self, section: str, data: dict, create: bool = False) -> None:
        if create:
            if not self._user_folder.exists():
                self._user_folder.mkdir()
            self._dictionary.update({section: data})

        if not self._dictionary.get(section):
            raise FileNotFoundError(f'File "{section}" not found')

        write_json(str(self._user_folder / f'{section}.json'), data)
        self._dictionary[section] = data

    @property
    def root(self):
        return self._user_folder

import os.path
from pathlib import Path
from typing import Any

from dotty_dict import Dotty

from cloudykit.abstracts.manager import IManager
from cloudykit.utils.files import read_json
from cloudykit.observers.filesystem import FileSystemObserver


class UserConfigManager(IManager):
    name = 'userconfig'

    def __init__(self) -> None:
        self._dictionary: Dotty = Dotty({})
        self._observer = FileSystemObserver()
        self._user_folder = Path(os.path.expanduser('~'))

    def mount(self, parent=None) -> None:
        if not (self._user_folder / '.crabs').exists():
            (self._user_folder / '.crabs').mkdir()
        for config in (self._user_folder / '.crabs').rglob('*.json'):
            if not self._dictionary.get(config.name):
                self._dictionary[config.stem] = {}
            self._dictionary[config.stem].update(**read_json(str(config)))

        self._observer.add_handler(str(self._user_folder / '.crabs'), parent.name)

    def unmount(self, parent=None) -> None:
        self._dictionary.pop(parent.name)
        self._observer.remove_handler(str(parent.root / 'configs'))

    def set(self, key, data: Any) -> None:
        self._dictionary[key] = data

    def get(self, key, default: Any = None) -> Any:
        return self._dictionary.get(key, default)

    @property
    def root(self):
        return self._user_folder

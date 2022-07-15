from typing import Any

from dotty_dict import Dotty

from cloudykit.abstracts.manager import IManager
from cloudykit.utils.files import read_json
from observers.filesystem import FileSystemObserver


class ConfigsManager(IManager):
    name = 'config'

    def __init__(self) -> None:
        self._dictionary = Dotty({})
        self._observer = FileSystemObserver()

    def mount(self, parent=None) -> None:
        for config in (parent.root / 'configs').rglob('*.json'):
            if not self._dictionary.get(config.name):
                self._dictionary[config.stem] = {}
            self._dictionary[config.stem].update(**read_json(str(config)))

        self._observer.add_handler(parent.root / 'configs', parent.name)

    def unmount(self, parent=None) -> None:
        self._dictionary.pop(parent.name)
        self._observer.remove_handler(str(parent.root / 'configs'))

    def set(self, key, data: Any) -> None:
        self._dictionary[key] = data

    def get(self, key, default: Any = None) -> Any:
        return self._dictionary.get(key, default)

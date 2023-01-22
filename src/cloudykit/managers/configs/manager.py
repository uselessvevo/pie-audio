import typing
from pathlib import Path
from dotty_dict import Dotty
from functools import lru_cache

from cloudykit.objects.manager import BaseManager
from cloudykit.system.types import PathConfig
from cloudykit.utils.files import read_json, write_json
from cloudykit.observers.filesystem import FileSystemObserver


class ConfigManager(BaseManager):
    name = "configs"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._dictionary: Dotty = Dotty({})
        self._observer = FileSystemObserver()

    def mount(self, *roots: PathConfig) -> None:
        for root_config in roots:
            for config in root_config.root.rglob(root_config.pattern):
                section = root_config.root.name if root_config.section_stem else root_config.section

                if not self._dictionary.get(config.name):
                    self._dictionary[section][config.stem] = {}
                self._dictionary[section][config.stem].update(**read_json(str(config)))
    
            self._observer.add_handler(str(root_config.root), str(root_config.root.name))

    def unmount(self, *args, **kwargs) -> None:
        self._dictionary = Dotty({})
        self._observer.remove_handlers(full_house=True)

    @lru_cache
    def get(self, section: str, key: typing.Any, default: typing.Any = None) -> typing.Any:
        return self._dictionary.get(f"{section}.{key}", default)

    def set(self, section: str, key: typing.Any, data: typing.Any) -> None:
        self._dictionary[section][key] = data

    def delete(self, section: str, key: typing.Any) -> None:
        del self._dictionary[section][key]

    def save(self, section: str, data: dict, create: bool = False) -> None:
        folder = self._dictionary.get(section)
        if not folder and not create:
            raise FileNotFoundError

        if create:
            if not folder.exists():
                folder.mkdir()
            self._dictionary.update({section: data})

        if not self._dictionary.get(section):
            raise FileNotFoundError(f"File {section} not found")

        write_json(str(folder / f"{section}.json"), data)
        self._dictionary[section] = data

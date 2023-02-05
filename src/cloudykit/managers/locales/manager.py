from pathlib import Path
from dotty_dict import Dotty

from cloudykit.system import PathConfig
from cloudykit.utils.files import read_json
from cloudykit.system import System
from cloudykit.managers.base import BaseManager


class LocalesManager(BaseManager):
    name = "locales"
    dependencies = ("configs",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._locale: str = System.registry.configs.get(
            "user", "locales.locale",
            default=System.config.DEFAULT_LOCALE
        )
        self._roots: set[PathConfig] = set()
        self._dictionary: Dotty = Dotty({})

    def mount(self, *roots: PathConfig) -> None:
        for root_config in roots:
            self._roots.add(root_config)
            files = (root_config.root / self._locale).rglob(root_config.pattern)
            for file in files:
                section: str = root_config.section

                if not self._dictionary.get(section):
                    self._dictionary[section] = {}

                if not self._dictionary.get(file.name):
                    self._dictionary[section][file.stem] = {}

                self._dictionary[file.stem].update(**read_json(str(file)))

    def unmount(self, *args, **kwargs) -> None:
        self._dictionary = Dotty({})

    def reload(self) -> None:
        self.unmount()
        self.mount(*self._roots)

    def get(self, section: str, key: str) -> str:
        value = self._dictionary.get(f"{section}.{key}")
        if not value:
            return key
        return value

    @property
    def locale(self):
        return self._locale

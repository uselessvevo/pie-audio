from pathlib import Path
from dotty_dict import Dotty

from piekit.managers.registry import Managers
from piekit.system.loader import Config
from piekit.utils.files import read_json
from piekit.managers.base import BaseManager
from piekit.structs.configs import PathConfig


class LocaleManager(BaseManager):
    name = "locales"
    dependencies = ("configs",)

    def __init__(self) -> None:
        super().__init__()

        self._locale: str = Managers.configs.get(
            "user", "locales.locale",
            default=Config.DEFAULT_LOCALE
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

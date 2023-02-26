from pathlib import Path
from typing import Union

from piekit.utils.files import read_json
from piekit.system.loader import Config
from piekit.managers.base import BaseManager
from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers, Sections


class LocaleManager(BaseManager):
    name = SysManagers.Locales
    dependencies = (SysManagers.Configs,)

    def __init__(self) -> None:
        super().__init__()

        self._locale: str = Managers.configs.get(
            "user", "locales.locale",
            default=Config.DEFAULT_LOCALE
        )
        self._roots: set[Path] = set()
        self._translations: dict[str, dict[str, str]] = {}

    def mount(self) -> None:
        # Read app/user configuration
        self._read_root_translations(Config.APP_ROOT, Sections.Shared)
        self._read_root_translations(Config.USER_ROOT, Sections.User)

        # Read plugin configuration
        self._read_plugin_translations(Config.APP_ROOT / Config.PLUGINS_FOLDER)
        self._read_plugin_translations(Config.USER_ROOT / Config.USER_PLUGINS_FOLDER)

    def _read_root_translations(self, folder: Path, section: Union[str, Sections] = None) -> None:
        self._roots.add(folder)

        for file in (folder / Config.LOCALES_FOLDER / self._locale).rglob("*.json"):
            section = section if section else file.parent.name
            if not self._translations.get(section):
                self._translations[section] = {}

            self._translations[file.stem].update(**read_json(str(file)))

    def _read_plugin_translations(self, folder: Path) -> None:
        for package in folder.iterdir():
            self._roots.add(package)

            for file in (package / Config.LOCALES_FOLDER / self._locale).rglob("*.json"):
                if not self._translations.get(file.name):
                    self._translations[file.stem] = {}

                self._translations[file.stem].update(**read_json(str(file)))

    def unmount(self, *args, **kwargs) -> None:
        self._translations = {}

    def reload(self) -> None:
        self.unmount()
        self.mount()

    def get(self, section: str, key: str) -> str:
        if section not in self._translations:
            return key

        return self._translations[section].get(key, key)

    @property
    def locale(self):
        return self._locale

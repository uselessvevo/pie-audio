from pathlib import Path

from piekit.utils.files import read_json
from piekit.globals import Global
from piekit.managers.base import PluginBaseManager
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager, Section


class LocaleManager(PluginBaseManager):
    name = SysManager.Locales

    def __init__(self) -> None:
        self._locale: str = Managers(SysManager.Configs).get(
            scope=Section.Root,
            section=Section.User,
            key="locale.locale",
            default=Global.DEFAULT_LOCALE
        )
        self._roots: set[Path] = set()
        self._translations: dict[str, dict[str, str]] = {}

    def init(self) -> None:
        # Read app/user configuration
        self._roots.add(Global.APP_ROOT)

        for file in (Global.APP_ROOT / Global.LOCALES_FOLDER / self._locale).rglob("*.json"):
            section = Section.Shared
            if not self._translations.get(section):
                self._translations[section] = {}

            self._translations[file.stem].update(**read_json(str(file)))

    def init_plugin(self, plugin_folder: Path) -> None:
        for folder in plugin_folder.iterdir():
            self._roots.add(folder)

            for file in (folder / Global.LOCALES_FOLDER / self._locale).rglob("*.json"):
                if not self._translations.get(file.name):
                    self._translations[file.stem] = {}

                self._translations[file.stem].update(**read_json(str(file)))

    def shutdown(self, *args, **kwargs) -> None:
        self._translations = {}

    def reload(self) -> None:
        self.shutdown()
        self.init()

    def get(self, section: str, key: str) -> str:
        if section not in self._translations:
            return key

        return self._translations[section].get(key, key)

    @property
    def locale(self):
        return self._locale

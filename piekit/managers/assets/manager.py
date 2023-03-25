from functools import lru_cache
from pathlib import Path
from typing import Any, Union

from PyQt5.QtGui import QIcon

from piekit.managers.assets.utils import setSvgColor
from piekit.managers.base import BaseManager
from piekit.managers.registry import Managers
from piekit.managers.structs import Sections
from piekit.managers.structs import SysManagers, DirectoryType
from piekit.system.loader import Config


class AssetsManager(BaseManager):
    name = SysManagers.Assets
    dependencies = (SysManagers.Configs,)

    def __init__(self) -> None:
        super().__init__()

        self._roots: set[Path] = set()
        self._dictionary: dict = dict()
        self._theme = Managers.get(SysManagers.Configs).get("user", "assets.theme")
        self._assets_folder = Config.APP_ROOT / Config.ASSETS_FOLDER
        self._themes = []

        theme_folders = tuple(i for i in (self._assets_folder / "themes").glob("*") if i.is_dir())
        for theme in theme_folders:
            self._themes.append(theme.name)

        if not self._theme and theme_folders:
            self._theme = self._themes[0]

    def mount(self) -> None:
        # Read app/user configuration
        self._read_root_assets(Config.APP_ROOT, Sections.Shared)
        self._read_root_assets(Config.USER_ROOT, Sections.User)

        # Read plugin configuration
        self._read_plugin_assets(Config.APP_ROOT / Config.PLUGINS_FOLDER)
        self._read_plugin_assets(Config.USER_ROOT / Config.USER_PLUGINS_FOLDER)

    def _read_root_assets(self, folder: Path, section: Union[str, Sections]) -> None:
        for file in (folder / Config.ASSETS_FOLDER / Config.THEMES_FOLDER / self._theme).rglob("*.*"):
            if file.suffix in Config.ASSETS_EXCLUDED_FORMATS:
                continue

            if file.is_dir() and DirectoryType in Config.ASSETS_EXCLUDED_FORMATS:
                continue

            if not self._dictionary.get(section):
                self._dictionary[section] = {}

            if not self._dictionary.get(file.name):
                self._dictionary[section][file.name] = {}

            self._dictionary[section].update({file.name: file.as_posix()})

    def _read_plugin_assets(self, folder: Path) -> None:
        for package in folder.iterdir():
            for file in (package / Config.ASSETS_FOLDER).rglob("*.*"):
                section = package.name

                if file.suffix in Config.ASSETS_EXCLUDED_FORMATS:
                    continue

                if file.is_dir() and DirectoryType in Config.ASSETS_EXCLUDED_FORMATS:
                    continue

                if not self._dictionary.get(section):
                    self._dictionary[section] = {}

                if not self._dictionary.get(file.name):
                    self._dictionary[section][file.name] = {}

                self._dictionary[section].update({file.name: file.as_posix()})

    @lru_cache
    def get(self, section: str, key: Any, default: Any = None) -> Any:
        try:
            return self._dictionary[section][key]
        except KeyError:
            self._logger.info(f"File {key} not found")
            return default

    @lru_cache
    def get_svg(self, *args, color: str = "#7cd162") -> QIcon:
        return setSvgColor(self.get(*args), color)

    @lru_cache
    def get_icon(self, section: str, key: Any, default: Any = None) -> QIcon:
        return QIcon(self.get(section, key, default))

    @property
    def root(self):
        return self._assets_folder

    @property
    def theme(self):
        return self._theme

    @property
    def themes(self):
        return self._themes

    getSvg = get_svg
    getIcon = get_icon

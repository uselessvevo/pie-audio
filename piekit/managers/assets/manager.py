from functools import lru_cache
from pathlib import Path
from typing import Any, Union

from PySide6.QtGui import QIcon

from piekit.managers.assets.utils import setSvgColor
from piekit.managers.base import BaseManager
from piekit.managers.registry import Managers
from piekit.managers.structs import Sections
from piekit.managers.structs import SysManagers, DirectoryType
from piekit.config import Config


class AssetsManager(BaseManager):
    name = SysManagers.Assets
    dependencies = (SysManagers.Configs,)

    def __init__(self) -> None:
        super().__init__()

        self._assets_dictionary: dict[str, Path] = {}
        self._current_theme = Managers(SysManagers.Configs).get_shared(Sections.User, "assets.theme")

        assets_folder: Path = Config.APP_ROOT / Config.ASSETS_FOLDER / "themes"
        theme_folders = list(i.name for i in assets_folder.iterdir() if i.is_dir())
        self._themes: list[str] = theme_folders

        if not self._current_theme and theme_folders:
            self._current_theme = theme_folders[0]

    def init(self) -> None:
        # Read app/user configuration
        self._read_root_assets(Config.APP_ROOT, Sections.Shared)
        self._read_root_assets(Config.USER_ROOT, Sections.User)

        # Read plugin configuration
        self._read_plugin_assets(Config.APP_ROOT / Config.PLUGINS_FOLDER)
        self._read_plugin_assets(Config.USER_ROOT / Config.USER_PLUGINS_FOLDER)

    def add(self, section: str, file: Path) -> None:
        if not self._check_file(file):
            self._logger.critical(f"Can't find file {file.as_posix()}")

        self._add_section(section, file)

    def _read_root_assets(self, folder: Path, section: Union[str, Sections]) -> None:
        for file in (folder / Config.ASSETS_FOLDER / Config.THEMES_FOLDER / self._current_theme).rglob("*.*"):
            if not self._check_file(file):
                continue

            self._add_section(section, file)

    def _read_plugin_assets(self, folder: Path) -> None:
        for package in folder.iterdir():
            for file in (package / Config.ASSETS_FOLDER).rglob("*.*"):
                if not self._check_file(file):
                    continue

                self._add_section(package.name, file)

    def _check_file(self, file: Path) -> bool:
        if file.suffix in Config.ASSETS_EXCLUDED_FORMATS:
            return False

        if file.is_dir() and DirectoryType in Config.ASSETS_EXCLUDED_FORMATS:
            return False

        return True

    def _add_section(self, section: str, file: Path) -> None:
        if not self._assets_dictionary.get(section):
            self._assets_dictionary[section] = {}

        if not self._assets_dictionary.get(file.name):
            self._assets_dictionary[section][file.name] = {}

        self._assets_dictionary[section].update({file.name: file.as_posix()})

    @lru_cache
    def get(self, section: str, key: Any, default: Any = None) -> Any:
        try:
            return self._assets_dictionary[section][key]
        except KeyError:
            self._logger.info(f"File {key} not found")
            return default

    @lru_cache
    def get_svg(self, *args, color: str = "#7cd162") -> QIcon:
        return setSvgColor(self.get(*args), color)

    @lru_cache
    def get_icon(self, section: str, key: Any, default: Any = None) -> QIcon:
        return QIcon(self.get(section, key, default))

    def get_theme(self) -> str:
        return self._current_theme

    def get_themes(self) -> list[str]:
        return self._themes

    getSvg = get_svg
    getIcon = get_icon
    getTheme = get_theme
    getThemes = get_themes
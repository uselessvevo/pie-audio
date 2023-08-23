from functools import lru_cache
from pathlib import Path
from typing import Any, Union

from PySide6.QtGui import QIcon

from piekit.managers.assets.utils import set_svg_color
from piekit.managers.base import PluginBaseManager
from piekit.managers.registry import Managers
from piekit.managers.structs import Section
from piekit.managers.structs import SysManager, DirectoryType
from piekit.config import Config
from piekit.utils.logger import logger


class AssetsManager(PluginBaseManager):
    name = SysManager.Assets

    def __init__(self) -> None:
        self._logger = logger
        self._assets_dictionary: dict[str, dict[str, Path]] = {}
        self._current_theme = Managers(SysManager.Configs).get(Section.Root, Section.User, "assets.theme")

        assets_folder: Path = Config.APP_ROOT / Config.ASSETS_FOLDER / Config.THEMES_FOLDER
        theme_folders = list(i.name for i in assets_folder.iterdir() if i.is_dir())
        self._themes: list[str] = theme_folders

        if not self._current_theme and theme_folders:
            self._current_theme = theme_folders[0]

    def init(self) -> None:
        # Read app/user configuration
        for file in (Config.APP_ROOT / Config.ASSETS_FOLDER / Config.THEMES_FOLDER / self._current_theme).rglob("*.*"):
            if not self._check_file(file):
                continue

            self._add_file(Section.Shared, file)

    def init_plugin(self, plugin_folder: Path) -> None:
        for file in (plugin_folder / Config.ASSETS_FOLDER).rglob("*.*"):
            if not self._check_file(file):
                continue

            self._add_file(plugin_folder.name, file)

    def _check_file(self, file: Path) -> bool:
        if file.suffix in Config.ASSETS_EXCLUDED_FORMATS:
            return False

        if file.is_dir() and DirectoryType in Config.ASSETS_EXCLUDED_FORMATS:
            return False

        return True

    def _add_file(self, section: Union[str, Section], file: Path) -> None:
        if not self._assets_dictionary.get(section):
            self._assets_dictionary[section] = {}

        if not self._assets_dictionary.get(file.name):
            self._assets_dictionary[section][file.name] = {}

        self._assets_dictionary[section].update({file.name: file.as_posix()})

    @lru_cache
    def get(self, section: Union[str, Section], key: Any, default: Any = None) -> Any:
        try:
            return self._assets_dictionary[section][key]
        except KeyError:
            self._logger.info(f"File {key} not found")
            return default

    @lru_cache
    def get_svg(self, *args, color: str = "#7cd162") -> QIcon:
        return set_svg_color(self.get(*args), color)

    def get_theme(self) -> str:
        return self._current_theme

    def get_themes(self) -> list[str]:
        return self._themes

    getSvg = get_svg
    getTheme = get_theme
    getThemes = get_themes

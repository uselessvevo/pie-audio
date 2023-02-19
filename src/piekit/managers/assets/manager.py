from functools import lru_cache
from typing import Any

from PyQt5.QtGui import QIcon

from piekit.managers.assets.utils import _setSvgColor
from piekit.managers.base import BaseManager
from piekit.managers.registry import Managers
from piekit.managers.types import PathConfig
from piekit.managers.types import SysManagers, DirectoryType
from piekit.system.loader import Config


class AssetsManager(BaseManager):
    name = "assets"
    dependencies = ("configs",)

    def __init__(self) -> None:
        super().__init__()

        self._roots: set[PathConfig] = set()
        self._dictionary: dict = dict()
        self._theme = Managers.get(SysManagers.Configs).get("user", "assets.theme")
        self._assets_folder = Config.APP_ROOT / Config.ASSETS_FOLDER
        self._themes = []

        theme_folders = tuple(i for i in (self._assets_folder / "themes").glob("*") if i.is_dir())

        if not self._theme and theme_folders:
            for theme in theme_folders:
                self._themes.append(theme.name)

            self._theme = self._themes[0]

    def mount(self, *roots: PathConfig) -> None:
        """
        Assets folder structure:

        assets \
        ... themes \
        ...... <theme name> \
        ......... fonts - folder with fonts
        ......... icons - folder with icons
        ......... palette.py - PyQt palette settings
        ......... theme.qss - output file from theme.template.qss
        ......... theme.template.qss - theme template file
        ......... variables.json - variables for theme.template.qss
        """
        for root_config in roots:
            self._roots.add(root_config)
            for file in (root_config.root / Config.THEMES_FOLDER / self._theme).rglob(root_config.pattern):
                section: str = root_config.section

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
    def getSvg(self, *args, color: str = "#7cd162") -> QIcon:
        return _setSvgColor(self.get(*args), color)

    @property
    def root(self):
        return self._assets_folder

    @property
    def theme(self):
        return self._theme

    @property
    def themes(self):
        return self._themes

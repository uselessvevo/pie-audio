from functools import lru_cache
from typing import Any

from cloudykit.system.manager import System
from cloudykit.system.types import PathConfig
from cloudykit.system.types import DirectoryType
from cloudykit.objects.manager import BaseManager


class AssetsManager(BaseManager):
    name = "assets"
    dependencies = ("configs",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._roots: set[PathConfig] = set()
        self._dictionary: dict = dict()
        self._theme = System.registry.configs.get("user", "assets.theme")
        self._assets_folder = System.root / System.config.ASSETS_FOLDER
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
            for file in (root_config.root / System.config.THEMES_FOLDER / self._theme).rglob(root_config.pattern):
                section: str = root_config.section

                if file.suffix in System.config.ASSETS_EXCLUDED_FORMATS:
                    continue

                if file.is_dir() and DirectoryType in System.config.ASSETS_EXCLUDED_FORMATS:
                    continue

                if not self._dictionary.get(section):
                    self._dictionary[section] = {}

                if not self._dictionary.get(file.name):
                    self._dictionary[section][file.stem] = {}

                self._dictionary.update({file.stem: file.as_posix()})

    @lru_cache
    def get(self, key: Any, default: Any = None) -> Any:
        return self._dictionary.get(key, default)

    @property
    def root(self):
        return self._assets_folder

    @property
    def theme(self):
        return self._theme

    @property
    def themes(self):
        return self._themes

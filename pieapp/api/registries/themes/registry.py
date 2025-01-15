import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Union

from PySide6.QtWidgets import QApplication

from pieapp.api.globals import Global
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.api.utils.files import read_json
from pieapp.api.utils.logger import logger
from pieapp.api.utils.qapp import get_application
from pieapp.api.utils.modules import import_by_path

from pieapp.api.models.scopes import Scope
from pieapp.api.registries.sysregs import SysRegistry
from pieapp.api.registries.base import BaseRegistry


class ThemeRegistryClass(BaseRegistry, ConfigAccessorMixin):
    name = SysRegistry.Themes

    def init(self) -> None:
        """
        Load root theme files

        Theme package structure:
            <theme name>:
            * <icons folder>
            * <fonts folder>
            * props.json - theme properties: colors and icons accent
            * theme.qss - style sheet template file
        """
        self._app: QApplication = None
        self._current_theme: str = None
        self._themes: list[str] = None

        # Registries
        self._files: dict[str, dict[str, Union[str, os.PathLike]]] = {}
        self._stylesheet: str = ""
        self._stylesheet_props: dict[str, str] = {}

        self._current_theme = self.get_app_config("config.theme", Scope.User, Global.DEFAULT_THEME)
        self._themes = self.load_themes()
        self.load_app_theme()
        self.load_plugins_theme(Global.APP_ROOT / Global.PLUGINS_DIR_NAME)
        self.load_plugins_theme(Global.USER_ROOT / Global.PLUGINS_DIR_NAME)

    def load_themes(self) -> list[str]:
        themes: list[str] = []
        for folder in (Global.APP_ROOT / Global.ASSETS_DIR_NAME).iterdir():
            if folder.is_dir() and not folder.name.startswith("__"):
                themes.append(folder.name)

        return themes

    def load_app_theme(self) -> None:
        theme_folder = Global.APP_ROOT / Global.ASSETS_DIR_NAME / self._current_theme
        for file in theme_folder.rglob("*.*"):
            if not self.check_file(file):
                continue

            self.add_file(Scope.Shared, theme_folder, file)

        self._stylesheet_props["THEME_ROOT"] = theme_folder.as_posix()

        self._app = get_application()
        if Global.USE_THEME:
            self.load_style_sheet(theme_folder)
        self.load_palette(theme_folder)

    def load_plugins_theme(self, plugins_folder: Path) -> None:
        """
        Load theme and icons in the plugin folder

        If `current_theme` folder doesn't exist manager will load icons from "flat" assets folder

        Args:
            plugins_folder (pathlib.Path): Plugins folder
        """
        for plugin_folder in plugins_folder.iterdir():
            theme_folder = plugin_folder / Global.ASSETS_DIR_NAME / self._current_theme
            if theme_folder.exists():
                icons_folder = theme_folder / "icons"
            else:
                icons_folder = plugin_folder / Global.ASSETS_DIR_NAME

            self._stylesheet_props[f"{plugin_folder.name.upper()}_PLUGIN"] = theme_folder.as_posix()

            for file in icons_folder.rglob("*.*"):
                if not self.check_file(file):
                    continue

                self.add_file(plugin_folder.name, theme_folder, file)

            if Global.USE_THEME:
                self.load_style_sheet(theme_folder)
            self.load_palette(theme_folder)
            self._app.set_style_sheet(self._stylesheet)

    def add_file(self, scope: str, theme_folder: Path, file: Path) -> None:
        """
        Add file to the files registry

        Args:
            scope (str|Scope): The file scope can be a plugin's name or `Section` item
            theme_folder (pathlib.Path): Theme full path
            file (pathlib.Path): File path
        """
        parts_index = len(theme_folder.parts)
        filename_key = file.parts[parts_index:]
        filename_key = "/".join(filename_key)

        if not self._files.get(scope):
            self._files[scope] = {}

        if not self._files[scope].get(filename_key):
            self._files[scope][filename_key] = {}

        self._files[scope][filename_key] = file.as_posix()

    def check_file(self, file: Path) -> bool:
        """
        Check if file is not a directory, or it has the right file format

        Args:
            file (pathlib.Path): A file path
        """
        if file.is_dir() or file.suffix not in Global.ICONS_ALLOWED_FORMATS:
            return False

        return True

    def parse_template(self, template_file: Path) -> None:
        """
        Parse template file
        """
        pattern = re.compile(r"@([A-Za-z0-9-_\.]+)")
        with open(str(template_file)) as lines:
            for line in lines:
                match_list = pattern.findall(line)
                for match in match_list:
                    if match in self._stylesheet_props:
                        line = line.replace(match, self._stylesheet_props.get(match))
                        line = line.replace("@", "")
                    else:
                        logger.debug(f"Can't find {match}/{line}")
                self._stylesheet += line

    def load_style_sheet(self, theme_folder: Path) -> None:
        theme_file = theme_folder / "theme.qss"
        if not theme_file.exists():
            return

        props_data = read_json(theme_folder / "props.json", raise_exception=False, default={})
        self._stylesheet_props.update(**props_data)
        self.parse_template(theme_file)

    def load_palette(self, theme_folder: Path) -> None:
        palette_file = theme_folder / "palette.py"
        if palette_file.exists():
            palette_module = import_by_path(str(palette_file))
            palette = palette_module.get_palette()
            self._app.set_palette(palette)

    def get(self, scope: str, key: str, default: Any = None) -> Any:
        """
        Get icon

        Args:
            scope (str|Scope): Section name
            key (str): Icon name
            default (Any): Default value if icon was not found
        """
        try:
            return self._files[scope][key]
        except KeyError:
            logger.debug(f"File {key} not found")
            return default

    def get_theme(self) -> str:
        return self._current_theme

    def get_themes(self) -> list[str]:
        return self._themes

    def get_theme_property(self, prop_name: str, default: Any = None) -> str:
        return self._stylesheet_props.get(prop_name, default)


ThemeRegistry = ThemeRegistryClass()

import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Union

from PySide6.QtWidgets import QApplication

from pieapp.api.gloader import Global
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.utils.files import read_json
from pieapp.utils.logger import logger
from pieapp.utils.qt import get_application
from pieapp.utils.modules import import_by_path

from pieapp.api.registries.models import Scope
from pieapp.api.registries.models import SysRegistry
from pieapp.api.registries.base import BaseRegistry


class ThemeRegistry(BaseRegistry, ConfigAccessorMixin):
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
        self._files: dict[str, dict[str, Path]] = {}
        self._stylesheet: str = ""
        self._stylesheet_props: dict[str, str] = {}

        self._current_theme = self.get_config("assets.theme", Scope.User, Global.DEFAULT_THEME)
        self._themes = self._get_themes()
        self._load_app_theme()
        self._load_plugins_theme(Global.APP_ROOT / Global.PLUGINS_FOLDER_NAME)
        self._load_plugins_theme(Global.USER_ROOT / Global.PLUGINS_FOLDER_NAME)

    def _get_themes(self) -> list[str]:
        themes: list[str] = []
        for folder in (Global.APP_ROOT / Global.ASSETS_FOLDER).iterdir():
            if folder.is_dir() and not folder.name.startswith("__"):
                themes.append(folder.name)

        return themes

    def _load_app_theme(self) -> None:
        theme_folder = Global.APP_ROOT / Global.ASSETS_FOLDER / self._current_theme
        for file in theme_folder.rglob("*.*"):
            if not self._check_file(file):
                continue

            self._add_file(Scope.Shared, theme_folder, file)

        self._stylesheet_props["THEME_ROOT"] = theme_folder.as_posix()

        self._app = get_application()
        if Global.USE_THEME:
            self._load_style_sheet(theme_folder)
        self._load_palette(theme_folder)

    def _load_plugins_theme(self, plugins_folder: Path) -> None:
        """
        Load theme and icons in the plugin folder

        If `current_theme` folder doesn't exist manager will load icons from "flat" assets folder

        Args:
            plugins_folder (pathlib.Path): Plugins folder
        """
        for plugin_folder in plugins_folder.iterdir():
            theme_folder = plugin_folder / Global.ASSETS_FOLDER / self._current_theme
            if theme_folder.exists():
                icons_folder = theme_folder / "icons"
            else:
                icons_folder = plugin_folder / Global.ASSETS_FOLDER

            self._stylesheet_props[f"{plugin_folder.name.upper()}_PLUGIN"] = theme_folder.as_posix()

            for file in icons_folder.rglob("*.*"):
                if not self._check_file(file):
                    continue

                self._add_file(plugin_folder.name, theme_folder, file)

            if Global.USE_THEME:
                self._load_style_sheet(theme_folder)
            self._load_palette(theme_folder)
            self._app.set_style_sheet(self._stylesheet)

    def _add_file(self, scope: Union[str, Scope], theme_folder: Path, file: Path) -> None:
        """
        Add file to the files registry

        Args:
            scope (str|Scope): The file scope can be a plugin's name or `Section` item
            theme_folder (pathlib.Path): Theme full path
            file (pathlib.Path): File path
        """
        if not self._files.get(scope):
            self._files[scope] = {}

        if not self._files.get(file.name):
            file_key = file.as_posix().replace(theme_folder.as_posix(), "")
            file_key = file_key.replace("/", "", 1)
            self._files[scope][file_key] = {}

        self._files[scope].update({f"{file.parent.name}/{file.name}": file.as_posix()})

    def _check_file(self, file: Path) -> bool:
        """
        Check if file is not a directory, or it has the right file format

        Args:
            file (pathlib.Path): A file path
        """
        if file.is_dir() or file.suffix not in Global.ICONS_ALLOWED_FORMATS:
            return False

        return True

    def _parse_template(self, template_file: Path) -> None:
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

    def _load_style_sheet(self, theme_folder: Path) -> None:
        theme_file = theme_folder / "theme.qss"
        if not theme_file.exists():
            return

        props_data = read_json(theme_folder / "props.json", raise_exception=False, default={})
        self._stylesheet_props.update(**props_data)
        self._parse_template(theme_file)

    def _load_palette(self, theme_folder: Path) -> None:
        palette_file = theme_folder / "palette.py"
        if palette_file.exists():
            palette_module = import_by_path(str(palette_file))
            palette = palette_module.get_palette()
            self._app.set_palette(palette)

    @lru_cache
    def get(self, scope: Union[str, Scope], key: str, default: Any = None) -> Any:
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

    getTheme = get_theme
    getThemes = get_themes
    getProperty = get_theme_property


Themes = ThemeRegistry()

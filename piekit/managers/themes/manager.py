import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Union

from PySide6.QtWidgets import QApplication

from piekit.globals import Global
from piekit.utils.files import read_json
from piekit.utils.logger import logger
from piekit.utils.core import get_application
from piekit.utils.modules import import_by_path

from piekit.managers.structs import Section
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager
from piekit.managers.base import PluginBaseManager


class ThemeManager(PluginBaseManager):
    """
    Theme package structure:
        <theme name>:
        * <icons folder>
        * <fonts folder>
        * props.json - theme properties: colors and icons accent
        * template.qss - style sheet template file
    """
    name = SysManager.Themes

    def __init__(self) -> None:
        self._logger = logger
        self._app: QApplication = None
        self._current_theme: str = None
        self._themes: list[str] = None

        # Registries
        self._icons: dict[str, dict[str, Path]] = {}
        self._icons_props: dict[str, str] = {}
        self._stylesheet: str = ""
        self._stylesheet_props: dict[str, str] = {}

    def init(self) -> None:
        """
        Load root theme files
        """
        self._current_theme = Managers(SysManager.Configs).get(
            scope=Section.Root,
            section=Section.User,
            key="assets.theme",
            default=Global.DEFAULT_THEME
        )
        self._themes = list(
            str(i.name) for i in
            (Global.APP_ROOT / Global.ASSETS_FOLDER / Global.THEMES_FOLDER).iterdir() if i.is_dir()
        )
        theme_folder = Global.APP_ROOT / Global.ASSETS_FOLDER / Global.THEMES_FOLDER / self._current_theme
        for file in theme_folder.rglob("*.*"):
            if not self._check_icon(file):
                continue

            self._add_icon(Section.Shared, file)

        self._app = get_application()
        self._load_style_sheet(theme_folder)
        self._load_palette(theme_folder)

    def init_plugin(self, plugin_folder: Path) -> None:
        theme_folder = plugin_folder / Global.ASSETS_FOLDER / Global.THEMES_FOLDER / self._current_theme
        if theme_folder.exists():
            icons_folder = theme_folder
        else:
            icons_folder = plugin_folder / Global.ASSETS_FOLDER

        for file in icons_folder.rglob("*.*"):
            if not self._check_icon(file):
                continue

            self._add_icon(plugin_folder.name, file)

        self._load_style_sheet(theme_folder)
        self._load_palette(theme_folder)
        self._app.set_style_sheet(self._stylesheet)

    def _add_icon(self, section: Union[str, Section], file: Path) -> None:
        """
        Add file to the files registry

        Args:
            section (str|Section): The file section can be a plugin's name or `Section` item
            file (pathlib.Path): A file path
        """
        if not self._icons.get(section):
            self._icons[section] = {}

        if not self._icons.get(file.name):
            self._icons[section][f"{file.parent.name}/{file.name}"] = {}

        self._icons[section].update({f"{file.parent.name}/{file.name}": file.as_posix()})

    def _check_icon(self, file: Path) -> bool:
        """
        Check if file is not a directory, or it has the right file format

        Args:
            file (pathlib.Path): A file path
        """
        if file.is_dir() or file.suffix not in Global.ICONS_ALLOWED_FORMATS:
            return False

        return True

    def _load_style_sheet(self, theme_folder: Path) -> None:
        theme_file = theme_folder / "theme.qss"
        if theme_file.exists():
            style_sheet = theme_file.read_text(encoding="utf-8")
            self._stylesheet += style_sheet

    def _load_palette(self, theme_folder: Path) -> None:
        palette_file = theme_folder / "palette.py"
        if palette_file.exists():
            palette_module = import_by_path(str(palette_file))
            palette = palette_module.get_palette()
            self._app.set_palette(palette)

    @lru_cache
    def get(self, section: Union[str, Section], key: str, default: Any = None) -> Any:
        """
        Get icon

        Args:
            section (str|Section): Section name
            key (str): Icon name
            default (Any): Default value if icon was not found
        """
        try:
            return self._icons[section][key]
        except KeyError:
            self._logger.info(f"File {key} not found")
            return default

    def get_theme(self) -> str:
        return self._current_theme

    def get_themes(self) -> list[str]:
        return self._themes

    getTheme = get_theme
    getThemes = get_themes

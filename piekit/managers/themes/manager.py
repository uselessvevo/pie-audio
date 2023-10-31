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
    name = SysManager.Themes

    def __init__(self) -> None:
        self._logger = logger
        self._app: QApplication = None
        self._current_theme: str = None
        self._themes: list[str] = None

        # Registries
        self._icons: dict[str, dict[str, Path]] = {}
        self._stylesheet: str = ""
        self._stylesheet_props: dict[str, str] = {}

    def init(self) -> None:
        """
        Load root theme files

        Theme package structure:
            <theme name>:
            * <icons folder>
            * <fonts folder>
            * props.json - theme properties: colors and icons accent
            * template.qss - style sheet template file
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
        """
        Load theme and icons in the plugin folder

        If `current_theme` folder doesn't exist manager will load icons from "flat" assets folder
        
        Args:
            plugin_folder (pathlib.Path): Plugin folder
        """
        theme_folder = plugin_folder / Global.ASSETS_FOLDER / Global.THEMES_FOLDER / self._current_theme
        if theme_folder.exists():
            icons_folder = theme_folder / "icons"
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

    def _parse_template(self, template_file: Path) -> None:
        """
        Parse template file
        """
        pattern = re.compile(r"@([A-Za-z0-9-]+)")
        with open(str(template_file)) as lines:
            for line in lines:
                match_list = pattern.findall(line)
                for match in match_list:
                    if match in self._stylesheet_props:
                        line = line.replace(match, self._stylesheet_props.get(match))
                        line = line.replace("@", "")
                self._stylesheet += line

    def _load_style_sheet(self, theme_folder: Path) -> None:
        theme_file = theme_folder / "theme.json"
        if not theme_file.exists():
            return

        theme_conf = read_json(theme_folder / "theme.json")
        if theme_conf.get("template") and theme_conf.get("properties"):
            props_data = theme_conf.get("properties")
            self._stylesheet_props.update(**props_data)
            self._parse_template(theme_folder / theme_conf["template"])

        elif theme_conf.get("theme"):
            theme_file = theme_folder / theme_conf.get("theme")
            if theme_file.exists():
                style_sheet = theme_file.read_text(encoding="utf-8")
                self._stylesheet += style_sheet
        
        else:
            self._logger.critical(f"Can't load theme: specify `template` or `theme` fields")

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

import copy
from pathlib import Path
from types import ModuleType
from typing import Union

from piekit.globals import Global
from piekit.utils.logger import logger
from piekit.utils.modules import import_by_path
from piekit.managers.base import BaseManager
from piekit.managers.structs import SysManager
from piekit.managers.confpages.structs import ConfigPage


class ConfigPageManager(BaseManager):
    name = SysManager.ConfigPages

    def __init__(self) -> None:
        super().__init__()
        self._logger = logger

        # <section name> : {page.name: <ConfigurationPage instance>, "children": [ConfigurationPage, ...], ...}
        self._pages: dict = {}

        self._pages_list: list[ConfigPage] = []

    def init(self) -> None:
        self._load_app_config_pages()
        self._load_plugins_config_pages(Global.APP_ROOT / Global.PLUGINS_FOLDER)
        self._load_plugins_config_pages(Global.USER_ROOT / Global.PLUGINS_FOLDER)

    def _load_app_config_pages(self) -> None:
        app_folder = Global.APP_ROOT / Global.CONF_PAGES_FOLDER
        if (app_folder / "confpage.py").exists():
            confpage_module: ModuleType = import_by_path(str(app_folder / "confpage.py"))
            confpage_instance = getattr(confpage_module, "main")()
            if confpage_instance:
                self._pages_list.append(confpage_instance)

    def _load_plugins_config_pages(self, plugins_folder: Path) -> None:
        for plugin_folder in plugins_folder.iterdir():
            if (plugin_folder / "confpage.py").exists():
                confpage_module: ModuleType = import_by_path(str(plugin_folder / "confpage.py"))
                confpage_instance = getattr(confpage_module, "main")()
                if confpage_instance:
                    self._pages_list.append(confpage_instance)

        pages: list[ConfigPage] = list(sorted(self._pages_list, key=lambda v: v.root is None))
        for page in reversed(pages):
            # Check if page is a category root item, and it doesn't exist in `self._pages`
            if not self._pages.get(page.name) and page.root is None:
                self._pages[page.name] = {"page": page, "children": set()}

            # Check if page is a child item and parent item does exist in `self._pages`
            elif page.root in self._pages:
                # Check if page is a child item and in its parent
                if page.name not in self._pages[page.root]["children"]:
                    self._pages[page.root]["children"].add(page)

    def shutdown(self, *args, **kwargs) -> None:
        self._pages = {}
        self._pages_list = []

    def get_page(self, section: str, page_name: str) -> ConfigPage:
        if section not in self._pages:
            raise KeyError(f"Configuration section {section} not found")

        if page_name not in self._pages[page_name]:
            raise KeyError(f"Configuration section {section} not found")

        return self._pages[section][page_name]

    def get_pages(self, section: str) -> list[ConfigPage]:
        return self._pages.get(section, [])

    def get_all_pages(self, as_list: bool = False) -> Union[dict[str, ConfigPage], list[ConfigPage]]:
        return self._pages_list if as_list else self._pages

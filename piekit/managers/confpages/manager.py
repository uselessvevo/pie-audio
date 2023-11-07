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
        self._collect_pages(Global.APP_ROOT / Global.CONF_PAGES_FOLDER)
        self._collect_pages(Global.APP_ROOT / Global.PLUGINS_FOLDER)
        self._collect_pages(Global.USER_ROOT / Global.PLUGINS_FOLDER)
        
        # Initialize pages
        for page in self._pages_list:
            page.init()

    def _collect_pages(self, plugin_folder: Path) -> None:
        for folder in plugin_folder.iterdir():
            if (folder / "confpage.py").exists():
                confpage_module: ModuleType = import_by_path(str(folder / "confpage.py"))
                confpage_instance = getattr(confpage_module, "main")()
                if confpage_instance:
                    self._pages_list.append(confpage_instance)

        page_instances: list[ConfigPage] = list(sorted(self._pages_list, key=lambda v: v.root is None))
        for page_instance in reversed(page_instances):
            # Check if page is a category root item, and it doesn't exist in `self._pages`
            if not self._pages.get(page_instance.name) and page_instance.root is None:
                self._pages[page_instance.name] = {"page": page_instance, "children": []}

            # Check if page is a child item and parent item does exist in `self._pages`
            elif page_instance.root in self._pages:
                # Check if page is a child item and in its parent
                if page_instance.name not in self._pages[page_instance.root]["children"]:
                    self._pages[page_instance.root]["children"].append(page_instance)

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
        if as_list:
            pages: list[ConfigPage] = []
            pages_copy: dict = copy.copy(self._pages)
            for page in pages_copy.values():
                children = page["children"]
                pages.append(page)
                for child in children:
                    pages.append(child)

            return pages

        return self._pages

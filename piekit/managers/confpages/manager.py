import copy
import inspect
from pathlib import Path
from types import ModuleType
from typing import Union

from piekit.config import Config
from piekit.exceptions import PieException
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
        # TODO: Collect all pages and ONLY than initialize them by calling `init` method
        self._read_root_confpages(Config.APP_ROOT / Config.CONF_PAGES_FOLDER)
        self._read_plugin_confpages(Config.APP_ROOT / Config.CONTAINERS_FOLDER)
        self._read_plugin_confpages(Config.APP_ROOT / Config.PLUGINS_FOLDER)
        self._read_plugin_confpages(Config.USER_ROOT / Config.USER_PLUGINS_FOLDER)
        self._populate_pages()

    def shutdown(self, *args, **kwargs) -> None:
        self._pages = {}
        self._pages_list = []

    def _populate_pages(self) -> None:
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

    def _collect_module_confpages(self, confpage_module: ModuleType) -> None:
        """
        Collect all ConfigurationPage instances from the given module

        Args:
            confpage_module (ModuleType): configuration page module instance
        """
        module_classes = (
            (_, m) for _, m in
            inspect.getmembers(confpage_module)
            if inspect.isclass(m)
            and m.__name__ != ConfigPage.__name__  # exclude `ConfigurationClass` class
        )

        for class_member in module_classes:
            if issubclass(class_member[1], ConfigPage):
                page_instance: ConfigPage = class_member[1]()
                page_instance.sig_restart_requested.connect(
                    lambda: self._notify_main_window_restart_request(page_instance)
                )
                try:
                    self._logger.debug(f"Initializing configuration page `{page_instance.name}`")
                    page_instance.init()
                except Exception as e:
                    raise PieException(
                        f"An error has been occurred while initializing conf page {page_instance.name}\n"
                        f"Error traceback: {e!s}"
                    )
                if page_instance.name not in self._pages_list:
                    self._pages_list.append(page_instance)

    def _notify_main_window_restart_request(self, page_instance: ConfigPage) -> None:
        page_instance.parent().sig_restart_requested.emit(page_instance.name)

    def _read_root_confpages(self, folder: Path) -> None:
        if (folder / "confpage.py").exists():
            confpage_module: ModuleType = import_by_path("confpage", str(folder / "confpage.py"))
            self._collect_module_confpages(confpage_module)

    def _read_plugin_confpages(self, plugins_folder: Path) -> None:
        for folder in plugins_folder.iterdir():
            if (folder / "confpage.py").exists():
                confpage_module: ModuleType = import_by_path("confpage", str(folder / "confpage.py"))
                self._collect_module_confpages(confpage_module)

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

import inspect
from pathlib import Path
from types import ModuleType
from typing import Union

from piekit.config import Config
from piekit.utils.modules import import_by_path
from piekit.managers.base import BaseManager
from piekit.managers.structs import Section, SysManager
from piekit.managers.confpages.structs import ConfigurationPage


class ConfigurationPageManager(BaseManager):
    name = SysManager.ConfigPages

    def __init__(self) -> None:
        super().__init__()

        # <category name> : {<page name>: <ConfigurationPage instance>}
        self._pages: dict[str, dict[str, ConfigurationPage]] = {}

    def init(self) -> None:
        for page_dict in Config.CONF_PAGES_CATEGORIES or []:
            self._pages[page_dict["name"]] = {"__title__": page_dict["title"], "pages": []}

        self._read_root_confpages(Config.APP_ROOT / Config.CONF_PAGES_FOLDER)
        self._read_plugin_confpages(Config.APP_ROOT / Config.CONTAINERS_FOLDER)
        self._read_plugin_confpages(Config.APP_ROOT / Config.PLUGINS_FOLDER)
        self._read_plugin_confpages(Config.APP_ROOT / Config.USER_PLUGINS_FOLDER)

    def shutdown(self) -> None:
        self._pages = {}

    def _collect_module_confpages(self, confpage_module: ModuleType) -> list[ConfigurationPage]:
        """
        Collect all ConfigurationPage instances from the given module

        Args:
            category (str|Section): category name
            confpage_module (ModuleType): configuration page module
        """
        for page in inspect.getmembers(confpage_module):
            if issubclass(page, ConfigurationPage):
                confpage_instance = confpage_module()
                self._pages[confpage_instance.category]["pages"].append({
                    confpage_instance.name: confpage_instance
                })

    def _read_root_confpages(self, folder: Path) -> None:
        self._pages[Section.Root] = {}
        confpage_module = import_by_path("confpage", str(folder / "confpage.py"))
        self._collect_module_confpages(confpage_module)

    def _read_plugin_confpages(self, plugins_folder: Path) -> None:
        for folder in plugins_folder.iterdir():
            confpage_module = import_by_path("confpage", str(folder / "confpage.py"))
            self._collect_module_confpages(confpage_module)

    def get(self, category: Union[str, None], page_name: str) -> ConfigurationPage:
        if category not in self._pages:
            raise KeyError(f"Configuration category {category} not found")

        if page_name not in self._pages[page_name]:
            raise KeyError(f"Configuration category {category} not found")

    def get_pages(self) -> dict:
        return self._pages

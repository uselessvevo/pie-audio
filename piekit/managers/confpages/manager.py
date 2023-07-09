import inspect
from pathlib import Path
from typing import Union
from types import ModuleType

from piekit.config import Config
from piekit.utils.logger import logger
from piekit.utils.modules import import_by_path
from piekit.managers.base import BaseManager
from piekit.managers.structs import Section, SysManager
from piekit.managers.confpages.structs import ConfigurationPage


class ConfigPageManager(BaseManager):
    name = SysManager.ConfigPages

    def __init__(self) -> None:
        super().__init__()
        self._logger = logger

        # <category name> : {<page name>: <ConfigurationPage instance>}
        self._pages: dict[str, dict[str, ConfigurationPage]] = {}

    def init(self) -> None:
        self._read_root_confpages(Config.APP_ROOT / Config.CONF_PAGES_FOLDER)
        self._read_plugin_confpages(Config.APP_ROOT / Config.CONTAINERS_FOLDER)
        self._read_plugin_confpages(Config.APP_ROOT / Config.PLUGINS_FOLDER)
        self._read_plugin_confpages(Config.APP_ROOT / Config.USER_PLUGINS_FOLDER)

    def shutdown(self, *args, **kwargs) -> None:
        self._pages = {}

    def _collect_module_confpages(self, confpage_module: ModuleType) -> None:
        """
        Collect all ConfigurationPage instances from the given module

        Args:
            confpage_module (ModuleType): configuration page module instance
        """
        module_classes = (
            (_, m) for _, m in
            inspect.getmembers(confpage_module) if inspect.isclass(m)
            and m.__name__ != ConfigurationPage.__name__  # exclude `ConfigurationClass` class
        )
        for class_member in module_classes:
            if issubclass(class_member[1], ConfigurationPage):
                page_instance = class_member[1]()
                self._logger.debug(f"Initializing configuration page `{page_instance.name}`")
                self._pages[page_instance.category].update({
                    page_instance.name: page_instance
                })

    def _read_root_confpages(self, folder: Path) -> None:
        self._pages[Section.Root] = {}
        if (folder / "confpage.py").exists():
            page_instance: ModuleType = import_by_path("confpage", str(folder / "confpage.py"))
            self._collect_module_confpages(page_instance)

    def _read_plugin_confpages(self, plugins_folder: Path) -> None:
        for folder in plugins_folder.iterdir():
            if (folder / "confpage.py").exists():
                confpage_module = import_by_path("confpage", str(folder / "confpage.py"))
                self._collect_module_confpages(confpage_module)

    def get(self, category: Union[str, None], page_name: str) -> ConfigurationPage:
        if category not in self._pages:
            raise KeyError(f"Configuration category {category} not found")

        if page_name not in self._pages[page_name]:
            raise KeyError(f"Configuration category {category} not found")

        return self._pages[category][page_name]

    def get_pages(self) -> dict:
        return self._pages

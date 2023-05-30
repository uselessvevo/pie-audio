from piekit.managers.base import BaseManager
from piekit.managers.structs import SysManager
from piekit.managers.confpages.structs import ConfigurationPage


class ConfigurationPageManager(BaseManager):
    name = SysManager.ConfigPages

    def __init__(self) -> None:
        super().__init__()

        self._sections: dict[str, str] = {}
        self._pages: dict[str, dict[str, ConfigurationPage]] = {}

    def add_section(self, section: str) -> None:
        if section in self._pages:
            raise KeyError(f"Section {section} is already registered")

        self._pages[section] = {}

    def remove_section(self, section: str) -> None:
        if section not in self._pages:
            raise KeyError(f"Section {section} doesn't exist")

        del self._pages[section]

    def add_page(self, section: str, page: ConfigurationPage) -> None:
        if section not in self._pages:
            raise KeyError(f"Section {section} is already registered")

        if page not in self._pages[section]:
            raise KeyError(f"Page {section}.{page} doesn't exist")

        self._pages[section] = {page: {}}

    def remove_page(self, section: str, page: ConfigurationPage) -> None:
        pass

    def get_all_sections(self) -> list[str]:
        pass

    def get_all_pages(self) -> list[ConfigurationPage]:
        pass

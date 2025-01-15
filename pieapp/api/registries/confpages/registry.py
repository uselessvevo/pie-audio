from typing import Any

from pieapp.api.exceptions import PieError
from pieapp.api.plugins import ConfigPage
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.sysregs import SysRegistry


class ConfigPageRegistryClass(BaseRegistry):
    name = SysRegistry.ConfigPages

    def init(self) -> None:
        self._config_pages: dict[str, ConfigPage] = {}

    def restore(self, *args, **kwargs):
        self._config_pages = {}

    def add(self, name: str, page: ConfigPage) -> ConfigPage:
        self._config_pages[name] = page
        return page

    def contains(self, name: str) -> bool:
        return name in self._config_pages.keys()

    def get(self, name: str) -> ConfigPage:
        if name not in self._config_pages:
            raise PieError(f"Can't find page \"{name}\"")

        return self._config_pages[name]

    def remove(self, name: str) -> None:
        if name not in self._config_pages:
            raise PieError(f"ConfigPage \"{name}\" not found")

        del self._config_pages[name]

    def update(self, new_name: str, new_page_class: ConfigPage) -> None:
        self._config_pages[new_name] = new_page_class

    def items(self, as_list: bool = False) -> list[Any]:
        return list(self._config_pages.items()) if as_list else self._config_pages.items()

    def values(self, as_list: bool = True):
        return list(self._config_pages.values()) if as_list else self._config_pages.values()


ConfigPageRegistry = ConfigPageRegistryClass()

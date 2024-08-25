from typing import Any

from PySide6.QtWidgets import QLayout

from pieapp.api.exceptions import PieException
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.models import SysRegistry


class ConfPageRegistry(BaseRegistry):
    name = SysRegistry.ConfigPages

    def init(self) -> None:
        self._config_pages: dict[str, QLayout] = {}

    def restore(self, *args, **kwargs):
        self._config_pages = {}

    def add(self, name: str, page) -> QLayout:
        if name in self._config_pages:
            raise PieException(f"ConfigPage \"{page}\" already exists")

        self._config_pages[name] = page
        return page

    def contains(self, name: str) -> bool:
        return name in self._config_pages.keys()

    def get(self, name: str) -> QLayout:
        if name not in self._config_pages:
            raise PieException(f"Can't find page \"{name}\"")

        return self._config_pages[name]

    def items(self) -> list[Any]:
        return list(self._config_pages.items())

    def values(self):
        return list(self._config_pages.values())

    def remove(self, name: str) -> None:
        if name not in self._config_pages:
            raise PieException(f"ConfigPage \"{name}\" not found")

        del self._config_pages[name]


ConfigPages = ConfPageRegistry()

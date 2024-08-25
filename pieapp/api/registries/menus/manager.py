from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar

from pieapp.widgets.menus import PieMenu
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.models import SysRegistry
from pieapp.api.exceptions import PieException


class MenuRegistry(BaseRegistry):
    name = SysRegistry.Menus

    def init(self):
        self._bars: dict[str, QMenuBar] = {}

        # Menu mapping
        self._menus: dict[str, dict[str, PieMenu]] = {}

        # Menu items/actions mapping
        self._items: dict[str, dict[str, QAction]] = {}

    def add_menu_bar(
        self,
        name: str,
        menu_bar: QMenuBar
    ) -> QMenuBar:
        if name in self._bars:
            raise PieException(f"MenuBar {name} already registered")

        self._bars[name] = menu_bar
        return menu_bar

    def get_menu_bar(self, name: str) -> QMenuBar:
        if name not in self._bars:
            raise PieException(f"MenuBar {name} doesn't exist")

        return self._bars[name]

    def add_menu(
        self,
        scope: str,
        name: str,
        menu: PieMenu
    ) -> PieMenu:
        if scope not in self._menus:
            self._menus[scope] = {}

        if name in self._menus:
            raise PieException(f"Menu {scope}.{name} already registered")

        self._menus[scope][name] = menu

        return menu

    def add_menu_item(
        self,
        scope: str,
        menu: str,
        name: str,
        item: QAction
    ) -> QAction:
        if scope not in self._items:
            self._items[scope] = {}

        if menu not in self._menus[scope]:
            raise PieException(f"Menu {scope}.{menu} not found")

        self._items[scope][name] = item

        return item

    def get_menu(self, scope: str, name: str) -> QMenu:
        if scope not in self._menus:
            raise PieException(f"Section {scope} doesn't exist")

        if name not in self._menus[scope]:
            raise PieException(f"Menu {scope}.{name} not found")

        return self._menus[scope][name]

    def get_menu_item(self, scope: str, name: str) -> QAction:
        if scope not in self._menus:
            raise PieException(f"Section {scope} doesn't exist")

        if name not in self._menus[scope]:
            raise PieException(f"MenuItem {scope}.{name} not found")

        return self._items[scope][name]


Menus = MenuRegistry()

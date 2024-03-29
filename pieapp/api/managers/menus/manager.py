from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar

from pieapp.widgets.menus import PieMenu
from pieapp.api.managers.base import BaseRegistry
from pieapp.api.managers.structs import SysRegistry
from pieapp.api.exceptions import PieException


class MenuRegistry(BaseRegistry):
    name = SysRegistry.Menus

    def __init__(self):
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
        section: str,
        name: str,
        menu: PieMenu
    ) -> PieMenu:
        if section not in self._menus:
            self._menus[section] = {}

        if name in self._menus:
            raise PieException(f"Menu {section}.{name} already registered")

        self._menus[section][name] = menu

        return menu

    def add_menu_item(
        self,
        section: str,
        menu: str,
        name: str,
        item: QAction
    ) -> QAction:
        if section not in self._items:
            self._items[section] = {}

        if menu not in self._menus[section]:
            raise PieException(f"Menu {section}.{menu} not found")

        self._items[section][name] = item

        return item

    def get_menu(self, section: str, name: str) -> QMenu:
        if section not in self._menus:
            raise PieException(f"Section {section} doesn't exist")

        if name not in self._menus[section]:
            raise PieException(f"Menu {section}.{name} not found")

        return self._menus[section][name]

    def get_menu_item(self, section: str, name: str) -> QAction:
        if section not in self._menus:
            raise PieException(f"Section {section} doesn't exist")

        if name not in self._menus[section]:
            raise PieException(f"MenuItem {section}.{name} not found")

        return self._items[section][name]

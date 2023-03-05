from __future__ import annotations

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu

from piekit.managers.structs import SysManagers
from piekit.widgets.menus import PieMenu
from piekit.managers.base import BaseManager
from piekit.system.exceptions import PieException


class MenuManager(BaseManager):
    name = SysManagers.Menus

    def __init__(self):
        super().__init__()

        # Menu mapping
        self._menus: dict[str, dict[str, PieMenu]] = {}

        # Menu items/actions mapping
        self._items: dict[str, dict[str, QAction]] = {}

    def add_menu(
        self,
        parent: QMenuBar,
        section: str,
        name: str,
        text: str,
        icon: QIcon = None
    ) -> PieMenu:
        if section not in self._menus:
            self._menus[section] = {}

        if name in self._menus:
            raise PieException(f"Menu {section}.{name} already registered")

        menu = PieMenu(parent=parent, name=name, text=text)
        if icon:
            menu.menuAction().setIconVisibleInMenu(True)
            menu.setIcon(icon)

        self._menus[section][name] = menu

        return menu

    def add_menu_item(
        self,
        section: str,
        menu: str,
        name: str,
        text: str,
        triggered: callable,
        icon: QIcon,
    ) -> QAction:
        if section not in self._items:
            self._items[section] = {}

        if menu not in self._menus[section]:
            raise PieException(f"Menu {section}.{menu} not found")

        menu_instance = self._menus[section][menu]
        action = menu_instance.addMenuItem(name, text, triggered, icon)

        self._items[section][name] = action

        return action

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

    addMenu = add_menu
    getMenu = get_menu
    addMenuItem = add_menu_item
    getMenuItem = get_menu_item

from __future__ import annotations

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu

from piekit.managers.types import SysManagers
from piekit.widgets.menus import Menu
from piekit.managers.base import BaseManager
from piekit.system.exceptions import PieException


class MenuManager(BaseManager):
    name = SysManagers.Menus

    def __init__(self):
        super().__init__()

        # Menu mapping
        self._menus: dict[str, dict[str, Menu]] = {}

        # Menu items/actions mapping
        self._items: dict[str, dict[str, QAction]] = {}

    def addMenu(
        self,
        section: str,
        parent: QMenuBar,
        name: str,
        text: str,
        icon: QIcon = None
    ) -> Menu:
        if section not in self._menus:
            self._menus[section] = {}

        if name in self._menus:
            raise PieException(f"Menu {name} already registered")

        menu = Menu(parent=parent, name=name, text=text)
        if icon:
            menu.menuAction().setIconVisibleInMenu(True)
            menu.setIcon(icon)

        self._menus[section][name] = menu

        return menu

    def addMenuItem(
        self,
        section: str,
        menu: str,
        name: str,
        text: str,
        icon: QIcon,
    ) -> QAction:
        if section not in self._items:
            self._items[section] = {}

        if menu not in self._menus[section]:
            raise PieException(f"Menu {menu} not found")

        menu_instance = self._menus[section][menu]
        action = menu_instance.addMenuItem(name, text, icon)

        self._items[section][name] = action

        return action

    def get_menu(self, section: str, name: str) -> QMenu:
        return self._menus[section][name]

    def get_menu_item(self, section: str, name: str) -> QAction:
        return self._items[section][name]

    getMenu = get_menu
    getMenuItem = get_menu_item

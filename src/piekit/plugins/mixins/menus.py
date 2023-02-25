from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu

from piekit.widgets.menus import Menu
from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers


class MenuMixin:

    def addMenu(
        self,
        section: str = None,
        parent: QMenuBar = None,
        name: str = None,
        text: str = None,
        icon: QIcon = None,
    ):
        return Managers(SysManagers.Menus).addMenu(section, parent, name, text, icon)

    def addMenuItem(
        self,
        section: str = None,
        menu: Menu = None,
        name: str = None,
        text: str = None,
        icon: QIcon = None,
    ) -> QAction:
        return Managers(SysManagers.Menus).addMenuItem(section, menu, name, text, icon)

    def getMenu(self, section: str, name: str) -> Menu:
        return Managers(SysManagers.Menus).getMenu(section, name)

    def getMenuItem(self, section: str, menu: str, name: str) -> QMenu:
        return Managers(SysManagers.Menus).getMenuItem(section, menu, name)

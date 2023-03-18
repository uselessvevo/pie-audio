from typing import Union

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QWidget

from piekit.widgets.menus import PieMenu, INDEX_END, INDEX_START
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections


class MenuAccessor:

    def addMenuBar(
        self,
        parent: QWidget = None,
        name: str = None
    ) -> QMenuBar:
        menuBar = QMenuBar(parent)
        return Managers(SysManagers.Menus).addMenuBar(name or Sections.Shared, menuBar)

    def getMenuBar(self, name: str) -> QMenuBar:
        return Managers(SysManagers.Menus).getMenuBar(name or Sections.Shared)

    def addMenu(
        self,
        parent: QMenuBar = None,
        section: str = None,
        name: str = None,
        text: str = None,
        icon: QIcon = None,
    ):
        menu = PieMenu(parent=parent, name=name, text=text)
        if icon:
            menu.menuAction().setIconVisibleInMenu(True)
            menu.setIcon(icon)

        return Managers(SysManagers.Menus).addMenu(section or Sections.Shared, name, menu)

    def addMenuItem(
        self,
        section: str = None,
        menu: str = None,
        name: str = None,
        text: str = None,
        triggered: callable = None,
        icon: QIcon = None,
        before: str = None,
        index: Union[int, INDEX_START, INDEX_END] = None
    ) -> QAction:
        manager = Managers(SysManagers.Menus)
        menuInstance = manager.getMenu(section, menu)
        menuInstance.addMenuItem(name, text, triggered, icon, before, index)
        return manager.addMenuItem(section or Sections.Shared, menu, name, menuInstance)

    def getMenu(self, section: str, name: str) -> PieMenu:
        return Managers(SysManagers.Menus).getMenu(section or Sections.Shared, name)

    def getMenuItem(self, section: str, menu: str, name: str) -> QAction:
        return Managers(SysManagers.Menus).getMenuItem(section, menu, name)

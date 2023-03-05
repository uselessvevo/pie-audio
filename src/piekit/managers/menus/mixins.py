from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu

from piekit.widgets.menus import PieMenu
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections


class MenuAccessor:

    def addMenu(
        self,
        parent: QMenuBar = None,
        section: str = None,
        name: str = None,
        text: str = None,
        icon: QIcon = None,
    ):
        return Managers(SysManagers.Menus).addMenu(parent, section or Sections.Shared, name, text, icon)

    def addMenuItem(
        self,
        section: str = None,
        menu: str = None,
        name: str = None,
        text: str = None,
        triggered: callable = None,
        icon: QIcon = None,
    ) -> QAction:
        return Managers(SysManagers.Menus).addMenuItem(section or Sections.Shared, menu, name, text, triggered, icon)

    def getMenu(self, section: str, name: str) -> PieMenu:
        return Managers(SysManagers.Menus).getMenu(section or Sections.Shared, name)

    def getMenuItem(self, section: str, menu: str, name: str) -> PieMenu:
        return Managers(SysManagers.Menus).getMenuItem(section, menu, name)

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction

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
        menu = PieMenu(parent=parent, name=name, text=text)
        if icon:
            menu.menuAction().setIconVisibleInMenu(True)
            menu.setIcon(icon)

        return Managers(SysManagers.Menus).addMenu(section or Sections.Shared, menu)

    def addMenuItem(
        self,
        section: str = None,
        menu: str = None,
        name: str = None,
        text: str = None,
        triggered: callable = None,
        icon: QIcon = None,
    ) -> QAction:
        manager = Managers(SysManagers.Menus)
        menu_instance = manager.get_menu(menu)
        menu_instance.addMenuItem(name, text, triggered, icon)
        return manager.addMenuItem(section or Sections.Shared, menu, name, menu_instance)

    def getMenu(self, section: str, name: str) -> PieMenu:
        return Managers(SysManagers.Menus).getMenu(section or Sections.Shared, name)

    def getMenuItem(self, section: str, menu: str, name: str) -> PieMenu:
        return Managers(SysManagers.Menus).getMenuItem(section, menu, name)

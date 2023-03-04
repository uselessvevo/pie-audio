from typing import Union

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QToolBar, QWidget

from piekit.widgets.menus import PieMenu
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections


class ToolBarAccessor:

    def addToolBar(self, parent: QObject, name: str = None) -> QToolBar:
        return Managers(SysManagers.ToolBars).addToolBar(parent, name or Sections.Shared)

    def addToolBarItem(
        self,
        section: str = None,
        name: str = None,
        item: QWidget = None
    ) -> QToolBar:
        return Managers(SysManagers.ToolBars).addItem(section or Sections.Shared, name, item)

    def getToolBarItem(self, section: str, name: str) -> PieMenu:
        return Managers(SysManagers.ToolBars).getMenuItem(section, name)

    def getToolBarItems(self, section: str, *names: str) -> list[QObject]:
        return Managers(SysManagers.ToolBars).getItems(section, *names)

    def getToolBar(self, section: str, name: str) -> QToolBar:
        return Managers(SysManagers.ToolBars).getToolBar(section or Sections.Shared, name)

    def getToolBars(self, section: str, *names: str) -> list[QToolBar]:
        return Managers(SysManagers.ToolBars).getToolBars(section, *names)

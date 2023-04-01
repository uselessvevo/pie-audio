from typing import Union

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QToolBar, QWidget

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections
from piekit.widgets.toolbars import PieToolBar


class ToolBarAccessor:

    def addToolBar(self, parent: QObject, name: str = None) -> QToolBar:
        toolbar = PieToolBar(parent=parent)
        return Managers(SysManagers.ToolBars).addToolBar(name or Sections.Shared, toolbar)

    def addToolBarItem(
        self,
        section: str = None,
        name: str = None,
        item: Union[QWidget, QAction] = None,
        after: str = None,
        before: str = None
    ) -> QToolBar:
        manager = Managers(SysManagers.ToolBars)
        toolbar: PieToolBar = manager.getToolBar(section)
        toolbar.addToolBarItem(name, item, after, before)
        return manager.addItem(section or Sections.Shared, name, item)

    def getToolBarItem(self, section: str, name: str) -> QWidget:
        return Managers(SysManagers.ToolBars).getItem(section, name)

    def getToolBarItems(self, section: str, *names: str) -> list[QObject]:
        return Managers(SysManagers.ToolBars).getItems(section, *names)

    def getToolBar(self, name: str) -> QToolBar:
        return Managers(SysManagers.ToolBars).getToolBar(name)

    def getToolBars(self, *names: str) -> list[QToolBar]:
        return Managers(SysManagers.ToolBars).getToolBars(*names)

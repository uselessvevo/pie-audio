from typing import Union

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar, QWidget

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections
from piekit.widgets.toolbars import PieToolBar


class ToolBarAccessor:

    def add_toolbar(self, parent: QObject, name: str = None) -> PieToolBar:
        toolbar = PieToolBar(parent=parent)
        return Managers(SysManagers.ToolBars).add_toolbar(name or Sections.Shared, toolbar)

    def add_toolbar_item(
        self,
        section: str = None,
        name: str = None,
        item: Union[QWidget, QAction] = None,
        after: str = None,
        before: str = None
    ) -> QWidget:
        manager = Managers(SysManagers.ToolBars)
        toolbar: PieToolBar = manager.get_toolbar(section)
        toolbar.add_toolbar_item(name, item, after, before)
        return manager.add_item(section or Sections.Shared, name, item)

    def get_toolbar_item(self, section: str, name: str) -> QWidget:
        return Managers(SysManagers.ToolBars).get_item(section, name)

    def get_toolbar_items(self, section: str, *names: str) -> list[QObject]:
        return Managers(SysManagers.ToolBars).get_items(section, *names)

    def get_toolbar(self, name: str) -> PieToolBar:
        return Managers(SysManagers.ToolBars).get_toolbar(name)

    def get_toolbars(self, *names: str) -> list[PieToolBar]:
        return Managers(SysManagers.ToolBars).get_toolbars(*names)

    addToolBar = add_toolbar
    getToolBar = get_toolbar
    getToolBars = get_toolbars
    addToolBarItem = add_toolbar_item
    getToolBarItem = get_toolbar_item
    getToolBarItems = get_toolbar_items

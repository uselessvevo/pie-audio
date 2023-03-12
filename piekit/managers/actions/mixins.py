from typing import Union

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QAction

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections


class ActionAccessor:

    def addAction(self, section: Union[str, Sections], parent: QObject, name: str = None) -> QAction:
        action = QAction(parent=parent)
        return Managers(SysManagers.Actions).addAction(section or Sections.Shared, name, action)

    def getAction(self, section: str, name: str) -> QAction:
        return Managers(SysManagers.ToolBars).getToolBar(section, name)

    def getActions(self, section: Union[str, Sections], *names: str) -> list[QAction]:
        return Managers(SysManagers.ToolBars).getToolBars(section, *names)

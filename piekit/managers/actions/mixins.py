from typing import Union

from PySide6.QtGui import QAction
from PySide6.QtCore import QObject

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections


class ActionAccessor:

    def add_action(self, section: Union[str, Sections], parent: QObject, name: str = None) -> QAction:
        action = QAction(parent=parent)
        return Managers(SysManagers.Actions).addAction(section or Sections.Shared, name, action)

    def get_action(self, section: str, name: str) -> QAction:
        return Managers(SysManagers.ToolBars).getToolBar(section, name)

    def get_actions(self, section: Union[str, Sections], *names: str) -> list[QAction]:
        return Managers(SysManagers.ToolBars).getToolBars(section, *names)

    addAction = add_action
    getAction = get_action
    getActions = get_actions

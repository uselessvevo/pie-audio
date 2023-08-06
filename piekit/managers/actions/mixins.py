from typing import Union

from PySide6.QtGui import QAction
from PySide6.QtCore import QObject

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager, Section


class ActionAccessorMixin:

    def add_action(self, section: Union[str, Section], parent: QObject, name: str = None) -> QAction:
        action = QAction(parent=parent)
        return Managers(SysManager.Actions).add_action(section or Section.Shared, name, action)

    def get_action(self, section: str, name: str) -> QAction:
        return Managers(SysManager.ToolBars).get_action(section, name)

    def get_actions(self, section: Union[str, Section], *names: str) -> list[QAction]:
        return Managers(SysManager.ToolBars).get_actions(section, *names)

    addAction = add_action
    getAction = get_action
    getActions = get_actions

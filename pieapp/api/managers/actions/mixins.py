from typing import Union

from PySide6.QtGui import QAction
from PySide6.QtCore import QObject

from pieapp.api.managers.registry import Registries
from pieapp.api.managers.structs import SysRegistry, Section


class ActionAccessorMixin:

    def add_action(self, section: Union[str, Section], parent: QObject, name: str = None) -> QAction:
        action = QAction(parent=parent)
        return Registries(SysRegistry.Actions).add(section or Section.Shared, name, action)

    def get_action(self, section: str, name: str) -> QAction:
        return Registries(SysRegistry.ToolBars).get(section, name)

    def get_actions(self, section: Union[str, Section], *names: str) -> list[QAction]:
        return Registries(SysRegistry.ToolBars).get_items(section, *names)

from typing import Union

from PySide6.QtGui import QAction
from PySide6.QtCore import QObject

from pieapp.api.registries.registry import Registry
from pieapp.api.registries.models import SysRegistry, Scope


class ActionAccessorMixin:

    def add_action(self, scope: Union[str, Scope], parent: QObject, name: str = None) -> QAction:
        action = QAction(parent=parent)
        return Registry(SysRegistry.Actions).add(scope or Scope.Shared, name, action)

    def get_action(self, scope: str, name: str) -> QAction:
        return Registry(SysRegistry.ToolBars).get(scope, name)

    def get_actions(self, scope: Union[str, Scope], *names: str) -> list[QAction]:
        return Registry(SysRegistry.ToolBars).items(scope, *names)

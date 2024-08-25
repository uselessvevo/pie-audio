from typing import Union

from PySide6.QtGui import QAction
from PySide6.QtCore import QObject

from pieapp.api.registries.actions.manager import Actions
from pieapp.api.registries.models import Scope
from pieapp.api.registries.toolbars.manager import ToolBars


class ActionAccessorMixin:

    def add_action(self, scope: Union[str, Scope], parent: QObject, name: str = None) -> QAction:
        action = QAction(parent=parent)
        return Actions.add(scope or Scope.Shared, name, action)

    def get_action(self, scope: str, name: str) -> QAction:
        return ToolBars.get(scope, name)

    def get_actions(self, scope: Union[str, Scope], *names: str) -> list[QAction]:
        return ToolBars.items(scope, *names)

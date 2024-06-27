from __future__ import annotations

from typing import Union

from PySide6.QtGui import QAction

from pieapp.api.registries.models import Scope
from pieapp.api.registries.models import SysRegistry
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.exceptions import PieException
from pieapp.helpers.logger import logger


class ActionRegistry(BaseRegistry):
    name = SysRegistry.Actions

    def __init__(self) -> None:
        self._logger = logger
        self._actions: dict[str, QAction] = {}

    def add(
        self,
        scope: Union[str, Scope],
        name: str,
        action: QAction
    ) -> QAction:
        if scope not in self._actions:
            self._actions[scope] = {}

        if name in self._actions[scope]:
            raise PieException(f"Action {name} already registered")

        self._actions[scope][name] = action

        return action

    def get(
        self,
        scope: Union[str, Scope],
        name: str
    ) -> QAction:
        if scope not in self._actions:
            raise PieException(f"Section {scope} not found")

        if name not in self._actions[scope]:
            raise PieException(f"Action item {scope}.{name} not found")

        return self._actions[scope][name]

    def items(
        self,
        scope: Union[str, Scope],
        *names: str
    ) -> list[QAction]:
        return [self.get(scope, n) for n in names]

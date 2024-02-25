from __future__ import annotations

from typing import Union

from PySide6.QtGui import QAction

from pieapp.api.managers.structs import Section
from pieapp.api.managers.structs import SysRegistry
from pieapp.api.managers.base import BaseRegistry
from pieapp.api.exceptions import PieException
from pieapp.helpers.logger import logger


class ActionRegistry(BaseRegistry):
    name = SysRegistry.Actions

    def __init__(self) -> None:
        self._logger = logger
        self._actions: dict[str, QAction] = {}

    def add(
        self,
        section: Union[str, Section],
        name: str,
        action: QAction
    ) -> QAction:
        if section not in self._actions:
            self._actions[section] = {}

        if name in self._actions[section]:
            raise PieException(f"Action {name} already registered")

        self._actions[section][name] = action

        return action

    def get(
        self,
        section: Union[str, Section],
        name: str
    ) -> QAction:
        if section not in self._actions:
            raise PieException(f"Section {section} not found")

        if name not in self._actions[section]:
            raise PieException(f"Action item {section}.{name} not found")

        return self._actions[section][name]

    def get_items(
        self,
        section: Union[str, Section],
        *names: str
    ) -> list[QAction]:
        return [self.get(section, n) for n in names]

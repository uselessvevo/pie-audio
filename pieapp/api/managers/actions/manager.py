from __future__ import annotations

from typing import Union

from PySide6.QtGui import QAction

from pieapp.api.managers.structs import Section
from pieapp.api.managers.structs import SysManager
from pieapp.api.managers.base import BaseManager
from pieapp.api.exceptions import PieException
from pieapp.helpers.logger import logger


class ActionManager(BaseManager):
    name = SysManager.Actions

    def __init__(self) -> None:
        self._logger = logger
        self._actions: dict[str, QAction] = {}

    def add_action(
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

    def get_action(
        self,
        section: Union[str, Section],
        name: str
    ) -> QAction:
        if section not in self._actions:
            raise PieException(f"Section {section} not found")

        if name not in self._actions[section]:
            raise PieException(f"Action item {section}.{name} not found")

        return self._actions[section][name]

    def get_actions(
        self,
        section: Union[str, Section],
        *names: str
    ) -> list[QAction]:
        return [self.get_action(section, n) for n in names]
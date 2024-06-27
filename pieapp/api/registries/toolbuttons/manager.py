from __future__ import annotations

from typing import Union

from PySide6.QtWidgets import QToolButton

from pieapp.api.registries.models import Scope
from pieapp.api.registries.models import SysRegistry
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.exceptions import PieException


class ToolButtonRegistry(BaseRegistry):
    name = SysRegistry.ToolButton

    def __init__(self):
        # Menu items/actions mapping
        self._buttons: dict[str, dict[str, QToolButton]] = {}

    def add_tool_button(
        self,
        scope: Union[str, Scope],
        name: str,
        button: QToolButton
    ) -> QToolButton:
        if scope not in self._buttons:
            self._buttons[scope] = {}

        if name in self._buttons[scope]:
            raise PieException(f"ToolButton {name} already registered in {scope}")

        self._buttons[scope][name] = button

        return button

    def get_tool_button(self, scope: Union[str, Scope], name: str) -> QToolButton:
        if scope not in self._buttons:
            raise PieException(f"Section {scope} doesn't exist")

        if name not in self._buttons[scope]:
            raise PieException(f"ToolButton {scope}.{name} not found")

        return self._buttons[scope][name]

    def get_tool_buttons(self, scope: Union[str, Scope], *names: str) -> list[QToolButton]:
        return [self.get_tool_button(scope, n) for n in names]

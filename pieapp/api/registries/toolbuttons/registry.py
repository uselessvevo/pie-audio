from __future__ import annotations

from PySide6.QtWidgets import QToolButton

from pieapp.api.exceptions import PieError
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.sysregs import SysRegistry


class ToolButtonRegistryClass(BaseRegistry):
    name = SysRegistry.ToolButton

    def init(self):
        # Menu items/actions mapping
        self._buttons: dict[str, dict[str, QToolButton]] = {}

    def add(
        self,
        scope: str,
        name: str,
        button: QToolButton
    ) -> QToolButton:
        if scope not in self._buttons:
            self._buttons[scope] = {}

        if name in self._buttons[scope]:
            raise PieError(f"ToolButton {name} already registered in {scope}")

        self._buttons[scope][name] = button

        return button

    def get(self, scope: str, name: str) -> QToolButton:
        if scope not in self._buttons:
            raise PieError(f"Section {scope} doesn't exist")

        if name not in self._buttons[scope]:
            raise PieError(f"ToolButton {scope}.{name} not found")

        return self._buttons[scope][name]

    def values(self, scope: str, *names: str) -> list[QToolButton]:
        return [self.get(scope, n) for n in names]


ToolButtonRegistry = ToolButtonRegistryClass()

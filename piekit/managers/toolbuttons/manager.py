from __future__ import annotations

from typing import Union

from PySide6.QtWidgets import QToolButton

from piekit.managers.structs import Section
from piekit.managers.structs import SysManager
from piekit.managers.base import BaseManager
from piekit.exceptions import PieException


class ToolButtonManager(BaseManager):
    name = SysManager.ToolButton

    def __init__(self):
        # Menu items/actions mapping
        self._buttons: dict[str, dict[str, QToolButton]] = {}

    def add_tool_button(
        self,
        section: Union[str, Section],
        name: str,
        button: QToolButton
    ) -> QToolButton:
        if section not in self._buttons:
            self._buttons[section] = {}

        if name in self._buttons[section]:
            raise PieException(f"ToolButton {name} already registered in {section}")

        self._buttons[section][name] = button

        return button

    def get_tool_button(self, section: Union[str, Section], name: str) -> QToolButton:
        if section not in self._buttons:
            raise PieException(f"Section {section} doesn't exist")

        if name not in self._buttons[section]:
            raise PieException(f"ToolButton {section}.{name} not found")

        return self._buttons[section][name]

    def get_tool_buttons(self, section: Union[str, Section], *names: str) -> list[QToolButton]:
        return [self.get_tool_button(section, n) for n in names]

    addToolButton = add_tool_button
    getToolButton = get_tool_button
    getToolButtons = get_tool_buttons

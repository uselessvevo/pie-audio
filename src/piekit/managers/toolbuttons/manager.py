from __future__ import annotations

from typing import Union

from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolButton

from piekit.managers.structs import Sections
from piekit.managers.structs import SysManagers
from piekit.managers.base import BaseManager
from piekit.system.exceptions import PieException


class ToolButtonManager(BaseManager):
    name = SysManagers.ToolButton

    def __init__(self):
        super().__init__()

        # Menu items/actions mapping
        self._buttons: dict[str, dict[str, QToolButton]] = {}

    def add_tool_button(
        self,
        parent: QObject,
        section: Union[str, Sections],
        name: str,
        text: str = None,
        tooltip: str = None,
        icon: QIcon = None,
        only_icon: bool = False,
    ) -> QToolButton:
        if section not in self._buttons:
            self._buttons[section] = {}

        if name in self._buttons[section]:
            raise PieException(f"ToolButton {name} already registered in {section}")

        button = QToolButton(parent=parent)
        if icon:
            button.setIcon(icon)

        if tooltip:
            button.setToolTip(tooltip)

        if text:
            button.setText(text)

        if only_icon:
            button.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self._buttons[section][name] = button

        return button

    def get_tool_button(self, section: Union[str, Sections], name: str) -> QToolButton:
        if section not in self._buttons:
            raise PieException(f"Section {section} doesn't exist")

        if name not in self._buttons[section]:
            raise PieException(f"ToolButton {section}.{name} not found")

        return self._buttons[section][name]

    def get_tool_buttons(self, section: Union[str, Sections], *names: str) -> list[QToolButton]:
        return [self.get_tool_button(section, n) for n in names]

    addToolButton = add_tool_button
    getToolButton = get_tool_button
    getToolButtons = get_tool_buttons

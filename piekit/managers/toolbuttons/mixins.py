from __feature__ import snake_case

from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QObject, QSize
from PySide6.QtWidgets import QToolButton

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager, Section
from piekit.config import Global


class ToolButtonAccessorMixin:

    def add_tool_button(
        self,
        parent: QObject = None,
        section: Union[str, Section] = Section.Shared,
        name: str = None,
        text: str = None,
        tooltip: str = None,
        icon: QIcon = None,
        triggered: callable = None,
        onlyIcon: bool = False,
    ) -> QToolButton:
        tool_button = QToolButton(parent=parent)
        if icon:
            tool_button.set_icon(icon)

        if tooltip:
            tool_button.set_tool_tip(tooltip)

        if text:
            tool_button.set_tool_button_style(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            # tool_button.set_tool_button_style(Qt.ToolButtonStyle.ToolButtonIconOnly)
            tool_button.set_text(text)

        if triggered:
            tool_button.clicked.connect(triggered)

        if onlyIcon:
            tool_button.set_tool_button_style(Qt.ToolButtonStyle.ToolButtonIconOnly)

        tool_button.set_focus_policy(Qt.FocusPolicy.NoFocus)
        tool_button.set_icon_size(QSize(*Global.TOOL_BUTTON_ICON_SIZE))

        return Managers(SysManager.ToolButton).add_tool_button(section or Section.Shared, name, tool_button)

    def get_tool_buttons(self, section: str, *names: str) -> list[QObject]:
        return Managers(SysManager.ToolButton).get_tool_buttons(section, *names)

    def get_tool_button(self, section: str, name: str) -> QToolButton:
        return Managers(SysManager.ToolButton).get_tool_button(section or Section.Shared, name)

    addToolButton = add_tool_button
    getToolButton = get_tool_button
    getToolButtons = get_tool_buttons

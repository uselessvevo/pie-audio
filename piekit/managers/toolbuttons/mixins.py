from __feature__ import snake_case

from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QObject, QSize
from PySide6.QtWidgets import QToolButton

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager, Section
from piekit.globals import Global
from piekit.widgets.toolbutton import create_tool_button


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
        only_icon: bool = False,
        object_name: str = "WorkbenchToolButton"
    ) -> QToolButton:
        tool_button = create_tool_button(
            parent=parent, text=text, tooltip=tooltip,
            icon=icon, triggered=triggered, only_icon=only_icon,
            icon_size=Global.TOOL_BUTTON_ICON_SIZE, object_name=object_name
        )
        return Managers(SysManager.ToolButton).add_tool_button(section or Section.Shared, name, tool_button)

    def get_tool_buttons(self, section: str, *names: str) -> list[QObject]:
        return Managers(SysManager.ToolButton).get_tool_buttons(section, *names)

    def get_tool_button(self, section: str, name: str) -> QToolButton:
        return Managers(SysManager.ToolButton).get_tool_button(section or Section.Shared, name)

    addToolButton = add_tool_button
    getToolButton = get_tool_button
    getToolButtons = get_tool_buttons

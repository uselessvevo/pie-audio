from __feature__ import snake_case

from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QToolButton

from pieapp.api.globals import Global
from pieapp.api.managers.structs import Section
from pieapp.api.managers.structs import SysRegistry
from pieapp.api.managers.registry import Registries
from pieapp.widgets.toolbutton import create_tool_button


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
        object_name: str = None
    ) -> QToolButton:
        tool_button = create_tool_button(
            parent=parent, text=text, tooltip=tooltip,
            icon=icon, triggered=triggered, only_icon=only_icon,
            icon_size=Global.TOOL_BUTTON_ICON_SIZE, object_name=object_name
        )
        return Registries(SysRegistry.ToolButton).add_tool_button(section or Section.Shared, name, tool_button)

    def get_tool_buttons(self, section: str, *names: str) -> list[QObject]:
        return Registries(SysRegistry.ToolButton).get_tool_buttons(section, *names)

    def get_tool_button(self, section: str, name: str) -> QToolButton:
        return Registries(SysRegistry.ToolButton).get_tool_button(section or Section.Shared, name)

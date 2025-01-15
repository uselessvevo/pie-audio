from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QToolButton

from pieapp.api.globals import Global
from pieapp.api.models.scopes import Scope
from pieapp.api.registries.toolbuttons.registry import ToolButtonRegistry
from pieapp.widgets.toolbars.toolbutton import create_tool_button


class ToolButtonAccessorMixin:

    @staticmethod
    def add_tool_button(
        parent: QObject = None,
        scope: str = Scope.Shared,
        name: str = None,
        text: str = None,
        tooltip: str = None,
        icon: QIcon = None,
        triggered: callable = None,
        only_icon: bool = False,
        object_name: str = None
    ) -> QToolButton:
        tool_button = create_tool_button(
            parent=parent,
            text=text,
            tooltip=tooltip,
            icon=icon,
            triggered=triggered,
            only_icon=only_icon,
            icon_size=Global.TOOL_BUTTON_ICON_SIZE,
            object_name=object_name
        )
        return ToolButtonRegistry.add(scope or Scope.Shared, name, tool_button)

    @staticmethod
    def get_tool_buttons(scope: str, *names: str) -> list[QObject]:
        return ToolButtonRegistry.values(scope, *names)

    @staticmethod
    def get_tool_button(scope: str, name: str) -> QToolButton:
        return ToolButtonRegistry.get(scope or Scope.Shared, name)

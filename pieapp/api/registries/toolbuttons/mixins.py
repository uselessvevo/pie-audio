from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QToolButton

from pieapp.api.gloader import Global
from pieapp.api.registries.models import Scope
from pieapp.api.registries.models import SysRegistry
from pieapp.api.registries.registry import Registry
from pieapp.widgets.toolbutton import create_tool_button


class ToolButtonAccessorMixin:

    def add_tool_button(
        self,
        parent: QObject = None,
        scope: Union[str, Scope] = Scope.Shared,
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
        return Registry(SysRegistry.ToolButton).add_tool_button(scope or Scope.Shared, name, tool_button)

    def get_tool_buttons(self, scope: str, *names: str) -> list[QObject]:
        return Registry(SysRegistry.ToolButton).get_tool_buttons(scope, *names)

    def get_tool_button(self, scope: str, name: str) -> QToolButton:
        return Registry(SysRegistry.ToolButton).get_tool_button(scope or Scope.Shared, name)

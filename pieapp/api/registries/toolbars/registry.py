from __future__ import annotations

from typing import Union

from PySide6.QtWidgets import QWidget

from pieapp.api.models.scopes import Scope
from pieapp.api.exceptions import PieError
from pieapp.api.registries.sysregs import SysRegistry
from pieapp.api.registries.base import BaseRegistry
from pieapp.widgets.toolbars.toolbars import PieToolBar


class ToolBarRegistryClass(BaseRegistry):
    name = SysRegistry.ToolBars

    def init(self):
        # Dictionary of PieToolBar items
        self._toolbars: dict[str, PieToolBar] = {}

        # Dictionary of toolbar items
        self._toolbar_items: dict[str, dict[str, QWidget]] = {}

    def add_toolbar(self, toolbar_name: str, toolbar: PieToolBar) -> PieToolBar:
        if toolbar_name in self._toolbars:
            raise PieError(f"ToolBar {toolbar_name} already registered")

        self._toolbars[toolbar_name] = toolbar

        return toolbar
    
    def add_toolbar_item(self, toolbar_name: str, item_name: str, item_widget: QWidget) -> QWidget:
        if toolbar_name not in self._toolbar_items:
            self._toolbar_items[toolbar_name] = {}

        if not isinstance(item_widget, QWidget):
            raise PieError(f"ToolBar item must be QWidget based instance!")

        self._toolbar_items[toolbar_name][item_name] = item_widget
        return item_widget

    def get_toolbar_item(self, toolbar_name: str, item_name: str) -> QWidget:
        if toolbar_name not in self._toolbar_items:
            raise PieError(f"Section {toolbar_name} not found")

        if item_name not in self._toolbar_items[toolbar_name]:
            raise PieError(f"ToolBar item {toolbar_name}.{item_name} not found")

        return self._toolbar_items[toolbar_name][item_name]

    def get_toolbar_items(self, toolbar_name: str, *names: str) -> list[QWidget]:
        return [self.get_toolbar_item(toolbar_name, n) for n in names]

    def get_toolbar(self, toolbar_name: str) -> PieToolBar:
        if toolbar_name not in self._toolbars:
            raise PieError(f"ToolBar {toolbar_name} not found")

        return self._toolbars[toolbar_name]

    def get_toolbars(self, *toolbar_names: str) -> list[PieToolBar]:
        return [self.get_toolbar(n) for n in toolbar_names]


ToolBarRegistry = ToolBarRegistryClass()

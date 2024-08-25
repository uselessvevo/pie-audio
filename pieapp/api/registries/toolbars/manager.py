from __future__ import annotations

from typing import Union

from PySide6.QtWidgets import QWidget

from pieapp.api.registries.models import Scope
from pieapp.api.registries.models import SysRegistry
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.exceptions import PieException
from pieapp.widgets.toolbars import PieToolBar


class ToolBarRegistry(BaseRegistry):
    name = SysRegistry.ToolBars

    def init(self):
        # ToolBar mapping
        self._toolbars: dict[str, PieToolBar] = {}

        # ToolBar items
        self._items: dict[str, dict[str, QWidget]] = {}

    def add_toolbar(
        self,
        name: Union[str, Scope],
        toolbar: PieToolBar
    ) -> PieToolBar:
        if name in self._toolbars:
            raise PieException(f"ToolBar {name} already registered")

        self._toolbars[name] = toolbar

        return toolbar
    
    def add_item(
        self,
        scope: Union[str, Scope],
        name: str,
        item: QWidget
    ) -> QWidget:
        if scope not in self._items:
            self._items[scope] = {}

        if not isinstance(item, QWidget):
            raise PieException(f"ToolBar item must be QWidget based instance!")

        self._items[scope][name] = item
        return item

    def get_item(
        self,
        scope: Union[str, Scope],
        name: str
    ) -> QWidget:
        if scope not in self._items:
            raise PieException(f"Section {scope} not found")

        if name not in self._items[scope]:
            raise PieException(f"ToolBar item {scope}.{name} not found")

        return self._items[scope][name]

    def items(
        self,
        scope: Union[str, Scope],
        *names: str
    ) -> list[QWidget]:
        return [self.get_item(scope, n) for n in names]

    def get_toolbar(self, name: Union[str, Scope]) -> PieToolBar:
        if name not in self._toolbars:
            raise PieException(f"ToolBar {name} not found")

        return self._toolbars[name]

    def get_toolbars(
        self,
        *names: Union[str, Scope],
    ) -> list[PieToolBar]:
        return [self.get_toolbar(n) for n in names]


ToolBars = ToolBarRegistry()

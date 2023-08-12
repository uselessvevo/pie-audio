from __future__ import annotations

from typing import Union

from PySide6.QtWidgets import QWidget

from piekit.managers.structs import Section
from piekit.managers.structs import SysManager
from piekit.managers.base import BaseManager
from piekit.exceptions import PieException
from piekit.widgets.toolbars import PieToolBar


class ToolBarManager(BaseManager):
    name = SysManager.ToolBars

    def __init__(self):
        # ToolBar mapping
        self._toolbars: dict[str, PieToolBar] = {}

        # ToolBar items
        self._items: dict[str, dict[str, QWidget]] = {}

    def add_toolbar(
        self,
        name: Union[str, Section],
        toolbar: PieToolBar
    ) -> PieToolBar:
        if name in self._toolbars:
            raise PieException(f"ToolBar {name} already registered")

        self._toolbars[name] = toolbar

        return toolbar
    
    def add_item(
        self,
        section: Union[str, Section],
        name: str,
        item: QWidget
    ) -> QWidget:
        if section not in self._items:
            self._items[section] = {}

        if not isinstance(item, QWidget):
            raise PieException(f"ToolBar item must be QWidget based instance!")

        self._items[section][name] = item
        return item

    def get_item(
        self,
        section: Union[str, Section],
        name: str
    ) -> QWidget:
        if section not in self._items:
            raise PieException(f"Section {section} not found")

        if name not in self._items[section]:
            raise PieException(f"ToolBar item {section}.{name} not found")

        return self._items[section][name]

    def get_items(
        self,
        section: Union[str, Section],
        *names: str
    ) -> list[QWidget]:
        return [self.get_item(section, n) for n in names]

    def get_toolbar(self,  name: Union[str, Section]) -> PieToolBar:
        if name not in self._toolbars:
            raise PieException(f"ToolBar {name} not found")

        return self._toolbars[name]

    def get_toolbars(
        self,
        *names: Union[str, Section],
    ) -> list[PieToolBar]:
        return [self.get_toolbar(n) for n in names]

    addToolBar = add_toolbar
    addItem = add_item
    getItem = get_item
    getToolBar = get_toolbar
    getToolBars = get_toolbars

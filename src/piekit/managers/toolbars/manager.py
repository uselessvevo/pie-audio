from __future__ import annotations

from typing import Union
from collections import OrderedDict

from PyQt5.QtWidgets import QToolBar, QWidget

from piekit.managers.structs import Sections
from piekit.managers.structs import SysManagers
from piekit.managers.base import BaseManager
from piekit.system.exceptions import PieException


class ToolBarManager(BaseManager):
    name = SysManagers.ToolBars

    def __init__(self):
        super().__init__()

        # ToolBar mapping
        self._toolbars: dict[str, QToolBar] = {}

        # ToolBar items
        self._items: dict[str, OrderedDict[str, QWidget]] = {}

    def add_toolbar(
        self,
        parent: QWidget,
        name: Union[str, Sections]
    ) -> QToolBar:
        if name in self._toolbars:
            raise PieException(f"ToolBar {name} already registered")

        toolbar = QToolBar(parent=parent)
        self._toolbars[name] = toolbar

        return toolbar
    
    def add_item(
        self,
        section: Union[str, Sections],
        name: str,
        item: QWidget,
        before: QWidget = None,
    ) -> QToolBar:
        if section not in self._items:
            self._items[section] = OrderedDict({})

        if not isinstance(item, QWidget):
            raise PieException(f"ToolBar item must be QWidget based instance!")

        toolbar = self.get_toolbar(section)
        if before:
            toolbar.addWidget(item)
        else:
            toolbar.addWidget(item)

        self._items[section][name] = item
        return toolbar

    def get_item(
        self,
        section: Union[str, Sections],
        name: str
    ) -> QWidget:
        if section not in self._items:
            raise PieException(f"Section {section} not found")

        if name not in self._items[section]:
            raise PieException(f"ToolBar item {section}.{name} not found")

        return self._items[section][name]

    def get_items(
        self,
        section: Union[str, Sections],
        *names: str
    ) -> list[QWidget]:
        return [self.get_item(section, n) for n in names]

    def get_toolbar(self,  name: Union[str, Sections]) -> QToolBar:
        if name not in self._toolbars:
            raise PieException(f"ToolBar {name} not found")

        return self._toolbars[name]

    def get_toolbars(
        self,
        *names: Union[str, Sections],
    ) -> list[QToolBar]:
        return [self.get_toolbar(n) for n in names]

    addToolBar = add_toolbar
    addItem = add_item
    getItem = get_item
    getToolBar = get_toolbar
    getToolBars = get_toolbars


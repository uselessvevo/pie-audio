from __future__ import annotations

from typing import Union
from collections import OrderedDict

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QToolBar, QWidget

from piekit.managers.structs import Sections
from piekit.managers.structs import SysManagers
from piekit.managers.base import BaseManager
from piekit.system.exceptions import PieException



class PieToolbar(QToolBar):

    def __init__(self, parent: QObject = None, name: str = None) -> None:
        super().__init__(parent)

        # Toolbar name/id
        self._name = name

        # Toolbar's items
        self._items: OrderedDict[str, QObject] = OrderedDict({})

    def addToolBarItem(
        self,
        name: str,
        item: QObject,
        before: str = None,
    ) -> QObject:
        if name in self._items:
            raise PieException(f"ToolBar {name} already exist")

        self.addWidget(item)
        self._items

        return item

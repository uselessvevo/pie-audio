from __future__ import annotations

from collections import OrderedDict
from typing import Union, Any

from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QHBoxLayout, QWidget, QSizePolicy

from piekit.config.exceptions import PieException


class PieToolBar(QWidget):

    def __init__(self, parent: QObject = None, name: str = None) -> None:
        super().__init__(parent)

        # Toolbar name/id
        self._name = name

        # Toolbar's items
        self._items: OrderedDict[str, QObject] = OrderedDict({})

        self._keys: list[Any] = list(self._items.keys())

        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(50)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self._layout)

    def addToolBarItem(
        self,
        name: str,
        item: Union[QWidget, QAction],
        after: str = None,
        before: str = None
    ) -> QObject:
        if name in self._items:
            raise PieException(f"ToolBar {name} already registered")

        if after:
            index = self._keys.index(after) + 1
            self._layout.insertWidget(index, item, Qt.AlignmentFlag.AlignLeft)

        elif before:
            self._layout.insertWidget(self._keys.index(before), item, Qt.AlignmentFlag.AlignLeft)
        else:
            self._layout.addWidget(item, Qt.AlignmentFlag.AlignLeft)

        self._items[name] = item
        self._keys.append(name)

        return item

from __future__ import annotations
from __feature__ import snake_case

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

        self.set_fixed_height(50)
        self.set_contents_margins(0, 0, 0, 0)
        self.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        self._layout = QHBoxLayout()
        self._layout.set_contents_margins(0, 0, 0, 1)
        self._layout.set_alignment(Qt.AlignmentFlag.AlignLeft)
        self.set_layout(self._layout)

        self.set_object_name(name)
        self.set_attribute(Qt.WidgetAttribute.WA_StyledBackground)

    def add_toolbar_item(
        self,
        name: str,
        item: Union[QWidget, QAction],
        after: str = None,
        before: str = None
    ) -> QObject:
        if name in self._items:
            raise PieException(f"PieToolBar {name} already registered")

        if after:
            index = self._keys.index(after) + 1
            self._layout.insert_widget(index, item, Qt.AlignmentFlag.AlignLeft)

        elif before:
            self._layout.insert_widget(self._keys.index(before), item, Qt.AlignmentFlag.AlignLeft)
        else:
            self._layout.add_widget(item, Qt.AlignmentFlag.AlignLeft)

        self._items[name] = item
        self._keys.append(name)

        return item

    addToolBarItem = add_toolbar_item

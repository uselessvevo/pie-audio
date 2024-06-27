from __future__ import annotations
from __feature__ import snake_case

from collections import OrderedDict
from typing import Union, Any

from PySide6.QtGui import QAction
from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QWidget, QToolBar, QToolButton

from pieapp.api.exceptions import PieException


class PieToolBar(QToolBar):
    """ A really simplified horizontal toolbar-like layout """

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, parent: QObject = None, name: str = None) -> None:
        super().__init__(parent)

        self._name = name

        # Toolbar items
        self._items: OrderedDict[str, dict] = OrderedDict({})
        self._keys: list[Any] = list(self._items.keys())

        self.set_attribute(Qt.WidgetAttribute.WA_StyledBackground)

    def add_toolbar_item(
        self,
        name: str,
        item: Union[QWidget, QAction],
        after: str = None,
        before: str = None
    ) -> QObject:
        if name in self._items:
            raise PieException(f"PieToolBar \"{name}\" already registered")

        self._items[name] = {"item": item, "after": after, "before": before}
        self._keys.append(name)

        return item

    def _get_items_list(self) -> list[QAction, QToolButton]:
        items_list: list[QAction, QToolButton] = []
        for items_dict in self._items.values():
            if items_dict["after"]:
                index = self._keys.index(items_dict["after"]) + 1
                items_list.insert(index, items_dict["item"])

            elif items_dict["before"]:
                index = self._keys.index(items_dict["before"]) - 1
                items_list.insert(index, items_dict["item"])
            else:
                items_list.append(items_dict["item"])

        return items_list

    def call(self) -> None:
        items_list = self._get_items_list()
        for item in items_list:
            if isinstance(item, QAction):
                self.add_action(item)
            elif isinstance(item, QToolButton):
                self.add_widget(item)

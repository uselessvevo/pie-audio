from __future__ import annotations
from __feature__ import snake_case

from typing import Any

import dataclasses as dt

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QTabBar, QTabWidget

from pieapp.api.exceptions import PieError


class PieTabBar(QTabBar):

    def __init__(self, name: str, parent: QObject = None) -> None:
        super().__init__(parent)
        self._name = name
        self._parent = parent
        self._items: dict = {}

    @property
    def name(self) -> str:
        return self._name


@dt.dataclass(frozen=True)
class PieTabItem:
    widget: QWidget
    title: str


class PieTab(QTabWidget):
    # TODO: Add "on tab move" event to save tabs position/index

    def __init__(self, name: str, title: str, parent: QObject = None) -> None:
        super().__init__(parent)
        self._name = name
        self._title = title
        self._parent = parent
        self._items: dict = {}
        self._keys: list[Any] = list(self._items.keys())

    @property
    def name(self) -> str:
        return self._name

    @property
    def title(self) -> str:
        return self._title

    def add_item(
        self,
        tab_name: str,
        item_name: str,
        item_widget: QWidget,
        after: str = None,
        before: str = None
    ) -> QWidget:
        if tab_name not in self._items.keys():
            self._items[tab_name] = []

        self._items[tab_name].append({"item": item_widget, "after": after, "before": before})
        self._keys.append(item_name)
        return item_widget

    def _get_items_list(self) -> list[PieTabItem]:
        items_list: list[PieTabItem] = []
        for tab_items in self._items.values():
            for items_dict in tab_items:
                tab_widget_item = PieTabItem(items_dict["item"], self._title)
                if items_dict["after"]:
                    index = self._keys.index(items_dict["after"]) + 1
                    items_list.insert(index, tab_widget_item)

                elif items_dict["before"]:
                    index = self._keys.index(items_dict["before"]) - 1
                    items_list.insert(index, tab_widget_item)
                else:
                    items_list.append(tab_widget_item)

        return items_list

    def call(self) -> None:
        items_list = self._get_items_list()
        for item in items_list:
            self.add_tab(item.widget, item.title)

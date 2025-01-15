from __future__ import annotations
from __feature__ import snake_case

import copy
from typing import Union, Any

from PySide6.QtGui import QIcon
from PySide6.QtGui import QAction
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMenuBar, QMenu

from pieapp.api.exceptions import PieError


class PieMenuBar(QMenuBar):

    def __init__(self, parent: QObject = None) -> None:
        super(PieMenuBar, self).__init__(parent)
        self._menus: list[PieMenu] = []

    def add_pie_menu(self, menu: PieMenu):
        self.add_menu(menu)
        self._menus.append(menu)

    def call(self) -> None:
        for menu in self._menus:
            menu.call()


class PieMenu(QMenu):

    def __init__(
        self,
        parent: QMenuBar = None,
        name: str = None,
        text: str = None,
    ) -> None:
        self._name = name
        self._text = text

        self._items: dict[str, dict] = {}
        self._keys: list[Any] = list(self._items.keys())

        if text is not None:
            super().__init__(parent=parent, title=text)
        else:
            super().__init__(parent=parent)

    def add_menu_item(
        self,
        name: str,
        text: str,
        triggered: callable = None,
        icon: QIcon = None,
        before: str = None,
        after: str = None,
        index: Union[int] = None
    ) -> QAction:
        if name in self._items:
            raise PieError(f"Menu item {name} already registered")

        item = QAction(parent=self, text=text, icon=icon)
        if triggered:
            item.triggered.connect(triggered)

        self._items[name] = {"item": item, "after": after, "before": before, "index": index}
        self._keys.append(name)

        return item

    def _get_items_list(self) -> list:
        # A really shitty way to sort the list of dicts
        # But I don't really care... for now
        items_list = sorted(self._items.values(), key=lambda d: d.get("index") or 0)
        for index, item_dict in enumerate(items_list):
            if index == len(self._keys):
                break

            if item_dict.get("index") == -1:
                item_copy = copy.copy(item_dict)
                del items_list[index]
                item_copy["index"] = len(items_list)
                items_list.insert(item_copy["index"], item_copy)

            elif item_dict["after"]:
                index = self._keys.index(item_dict["after"])
                items_list.insert(index, item_dict)

            elif item_dict["before"]:
                index = self._keys.index(item_dict["before"]) - 1
                items_list.insert(index, item_dict)

        items_list = [i["item"] for i in items_list]
        return items_list

    def call(self) -> None:
        items_list = self._get_items_list()
        self.add_actions(items_list)

    def get_item(self, name: str) -> QAction:
        return self._items[name]["item"]

    @property
    def name(self) -> str:
        return self._name

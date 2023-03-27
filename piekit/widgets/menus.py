from __future__ import annotations

from typing import Union, Any

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

from piekit.system.exceptions import PieException


INDEX_END = type("INDEX_END", (), {})
INDEX_START = type("INDEX_START", (), {})
DEFAULT_INDEX = type("DEFAULT_INDEX", (), {})


class PieMenu(QMenu):

    def __init__(
        self,
        parent: QMenuBar = None,
        name: str = None,
        text: str = None,
    ) -> None:
        self._name = name
        self._text = text

        self._items: dict[str, QAction] = {}
        self._keys: list[Any] = list(self._items.keys())

        if text is not None:
            super().__init__(parent=parent, title=text)
        else:
            super().__init__(parent=parent)

    def addMenuItem(
        self,
        name: str,
        text: str,
        triggered: callable = None,
        icon: QIcon = None,
        before: str = None,
        index: Union[int, INDEX_START, INDEX_END] = None
    ) -> QAction:
        if name in self._items:
            raise PieException(f"Menu item {name} already registered")

        action = QAction(parent=self, text=text, icon=icon)
        if triggered:
            action.triggered.connect(triggered)

        self._items[name] = action
        self._keys.append(name)

        if isinstance(index, INDEX_START):
            index = self._items[self._keys[0]]
            self.insertAction(index, action)

        elif isinstance(index, INDEX_END):
            index = self._items[self._keys[-1]]
            self.insertAction(index, action)

        elif isinstance(index, int):
            index = self._items[self._keys[index]]
            self.insertAction(index, action)

        elif before:
            before = self._items[before]
            self.insertAction(before, action)

        else:
            self.addAction(action)

        return action

    def getItem(self, name: str) -> QAction:
        return self._items[name]

    @property
    def name(self) -> str:
        return self._name

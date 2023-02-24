from __future__ import annotations

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

from piekit.system.exceptions import PieException


class Menu(QMenu):

    def __init__(
        self,
        parent: QMenuBar = None,
        name: str = None,
        text: str = None,
    ) -> None:
        self._name = name
        self._text = text

        self._items: dict[str, QAction] = {}

        if text is not None:
            super().__init__(parent=parent, title=text)
        else:
            super().__init__(parent=parent)

    def addMenuItem(
        self,
        name: str,
        text: str,
        icon: QIcon = None
    ) -> QAction:
        if name in self._items:
            raise PieException(f"Menu item {name} already exist")

        action = QAction(parent=self, text=text, icon=icon)
        self.addAction(action)
        self._items[name] = action

        return action

    def getItem(self, name: str) -> QAction:
        return self._items[name]

    @property
    def name(self) -> str:
        return self._name

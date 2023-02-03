from cloudykit.system.manager import System
from cloudykit.managers.base import BaseManager

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut


class ShortcutsManager(BaseManager):

    def __init__(self, parent: "SystemManager") -> None:
        super().__init__(parent)

        self._shortcuts: dict[key, QShortcut] = {}

    def mount(self, shortcut: str, parent: "AppWindow" = None) -> None:
        pass

    
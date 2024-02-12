from PySide6.QtGui import QShortcut

from pieapp.api.exceptions import PieException
from pieapp.api.managers.base import BaseManager
from pieapp.api.managers.structs import SysManager


class ShortcutManager(BaseManager):
    name = SysManager.Shortcuts

    def __init__(self) -> None:
        self._shortcuts: dict[str, QShortcut] = {}

    def get(self, name: str) -> QShortcut:
        return self._shortcuts.get(name)

    def add(self, name: str, shortcut: QShortcut) -> None:
        self._shortcuts[name] = shortcut

    def remove(self, name: str) -> None:
        self._shortcuts.pop(name)

from PySide6.QtGui import QShortcut

from piekit.exceptions import PieException
from piekit.managers.base import BaseManager
from piekit.managers.structs import SysManager


class ShortcutManager(BaseManager):
    name = SysManager.Shortcuts

    def __init__(self) -> None:
        self._shortcuts: dict[str, QShortcut] = {}

    def get(self, name: str) -> QShortcut:
        if name not in self._shortcuts:
            raise PieException(f"Shortcut \"{name}\" not found")

        return self._shortcuts[name]

    def add(self, name: str, shortcut: QShortcut) -> None:
        if name in self._shortcuts:
            raise PieException(f"Shortcut \"{name}\" is already registered")

        self._shortcuts[name] = shortcut

    def remove(self, name: str) -> None:
        if name not in self._shortcuts:
            raise PieException(f"Shortcut \"{name}\" was not found")

        self._shortcuts.pop(name)

from typing import TypedDict

from PySide6.QtGui import QShortcut

from pieapp.api.managers.base import BaseRegistry
from pieapp.api.managers.structs import SysRegistry


class ShortcutDict(TypedDict):
    instance: QShortcut
    target_name: str
    title: str
    description: str


class ShortcutRegistry(BaseRegistry):
    name = SysRegistry.Shortcuts

    def __init__(self) -> None:
        self._shortcuts: dict[str, ShortcutDict] = {}

    def get(self, name: str) -> QShortcut:
        return self._shortcuts[name]["instance"]

    def add(self, name: str, shortcut: ShortcutDict) -> None:
        self._shortcuts[name] = shortcut

    def remove(self, name: str) -> None:
        self._shortcuts.pop(name)

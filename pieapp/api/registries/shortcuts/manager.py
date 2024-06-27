from typing import Any

from PySide6.QtGui import QShortcut

from pieapp.api.models.shortcuts import ShortcutDict
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.models import SysRegistry


class ShortcutRegistry(BaseRegistry):
    name = SysRegistry.Shortcuts

    def __init__(self) -> None:
        self._shortcuts: dict[str, ShortcutDict] = {}

    def get(self, name: str) -> QShortcut:
        if name in self._shortcuts:
            raise KeyError(f"Shortcut \"{name}\" was not found")

        return self._shortcuts[name]["shortcut"]

    def add(self, name: str, shortcut: QShortcut, target: str,
            title: str, shortcut_key: str, description: str, hidden: bool) -> None:
        """
        Register a shortcut for given target

        Args:
            name (str): Shortcut name
            shortcut (QShortcut): QShortcut instance
            target (str): Target
            title (str): Shortcut title
            description (str): Shortcut description
        """
        if name in self._shortcuts:
            raise KeyError(f"Shortcut \"{name}\" for target \"{target}\" is already registered")

        self._shortcuts[name] = {
            "shortcut": shortcut,
            "target": target,
            "shortcut_key": shortcut_key,
            "title": title,
            "description": description,
            "hidden": hidden
        }

    def remove(self, name: str) -> None:
        if name in self._shortcuts:
            raise KeyError(f"Shortcut \"{name}\" was not found")

        self._shortcuts.pop(name)

    def contains(self, name: str) -> bool:
        return name in self._shortcuts

    def items(self, *args, **kwargs) -> Any:
        return self._shortcuts.items()

    def values(self, *args, **kwargs) -> list[ShortcutDict]:
        return list(self._shortcuts.values())

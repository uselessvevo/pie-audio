from PySide6.QtCore import QObject
from PySide6.QtGui import QShortcut, QKeySequence

from pieapp.api.exceptions import PieError
from pieapp.api.models.shortcuts import ShortcutDict
from pieapp.api.registries.shortcuts.registry import ShortcutRegistry


class ShortcutAccessorMixin:

    def add_shortcut(
        self,
        name: str,
        shortcut: str,
        triggered: callable,
        target: QObject = None,
        title: str = None,
        description: str = None,
        hidden: bool = False
    ) -> None:
        name = f"{self.__class__.__name__}.{name}"
        if ShortcutRegistry.contains(name):
            raise PieError(f"Shortcut \"{name}/{shortcut}\" is already registered")

        shortcut_instance = QShortcut(QKeySequence(shortcut), target)
        shortcut_instance.activated.connect(triggered)
        target_name: str = getattr(target, "name", target.__class__.__name__)
        ShortcutRegistry.add(name, shortcut_instance, target_name, title, shortcut, description, hidden)

    def remove_shortcut(self, shortcut_name: str) -> None:
        ShortcutRegistry.remove(f"{self.__class__.__name__}.{shortcut_name}")

    @staticmethod
    def get_shortcuts() -> list[ShortcutDict]:
        return ShortcutRegistry.values()

    @staticmethod
    def contains_shortcut(name: str) -> bool:
        return ShortcutRegistry.contains(name)

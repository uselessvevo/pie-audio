from PySide6.QtCore import QObject
from PySide6.QtGui import QShortcut, QKeySequence
from pieapp.api.exceptions import PieException

from pieapp.api.managers.registry import Registries
from pieapp.api.managers.structs import SysRegistry


class ShortcutAccessorMixin:

    def get_shortcut(self, name: str) -> QShortcut:
        """
        A proxy method to retrieve QShortcut instance

        Args:
            name (str): Shortcut field name
        """
        return Registries(SysRegistry.Shortcuts).get(name)

    def add_shortcut(self, name: str, shortcut: str, triggered: callable, target: QObject = None) -> None:
        """
        A proxy method to add shortcut in the `target`

        Args:
            name (str): Shortcut field name
            shortcut (str): Shortcut sequence
            triggered (callable): What function to call when activating the shortcut
            target (QObject): On which object will the shortcut be called
        """
        shortcut_name = f"{target.__class__.__name__}.{name}"
        manager = Registries(SysRegistry.Shortcuts)
        if manager.get(shortcut_name):
            raise PieException(f"Shortcut \"{shortcut_name}\" is already registered")

        shortcut_instance = QShortcut(QKeySequence(shortcut), target or self)
        shortcut_instance.activated.connect(triggered)
        setattr(self, name, shortcut_instance)
        manager.add(shortcut_name, shortcut)

    def remove_shortcut(self, name: str, target: QObject = None) -> None:
        """
        A proxy method to remove shortcut by its field name from the `target`

        Args:
            name (str): Shortcut field name
            target (QObject): From which object will the shortcut be deleted
        """
        shortcut_name = f"{target.__class__.__name__}.{name}"
        manager = Registries(SysRegistry.Shortcuts)
        if manager.get(shortcut_name):
            raise PieException(f"Shortcut \"{shortcut_name}\" is already registered")

        shortcut_instance = QShortcut(QKeySequence(), target or self)
        delattr(self, name)
        manager.remove(shortcut_name)
        manager.add(shortcut_name, shortcut_instance)



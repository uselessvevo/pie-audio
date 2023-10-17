from PySide6.QtCore import QObject
from PySide6.QtGui import QShortcut, QKeySequence

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager


class ShortcutAccessorMixin:

    def get_shortcut(self, name: str) -> QShortcut:
        return Managers(SysManager.Shortcuts).get(name)

    def add_shortcut(self, name: str, shortcut: str, triggered: callable, target: QObject = None) -> None:
        shortcut_instance = QShortcut(QKeySequence("Ctrl+F"), target or self)
        shortcut_instance.activated.connect(triggered)
        setattr(self, name.replace("-", "_"), shortcut_instance)
        Managers(SysManager.Shortcuts).add(name, shortcut)

    def remove_shortcut(self, name: str, target: QObject = None) -> None:
        shortcut_instance = QShortcut(QKeySequence(), target or self)
        setattr(self, name, shortcut_instance)
        Managers(SysManager.Shortcuts).remove(name)
        Managers(SysManager.Shortcuts).add(name, shortcut_instance)

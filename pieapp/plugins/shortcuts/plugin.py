from __feature__ import snake_case

from PySide6.QtCore import QObject
from PySide6.QtGui import QShortcut, QKeySequence

from pieapp.api.plugins import PieObject
from pieapp.api.exceptions import PieException
from pieapp.api.managers.locales.helpers import translate
from pieapp.api.structs.plugins import Plugin


class ShortcutManager(PieObject):
    name = Plugin.Shortcut

    @staticmethod
    def get_name() -> str:
        return translate("Shortcut")

    @staticmethod
    def get_description() -> str:
        return translate("Shortcut manager")

    def init(self) -> None:
        # TODO: Add shortcuts manifest file
        self._shortcuts: dict = {}

    def add_shortcut(
        self,
        name: str,
        shortcut: str,
        triggered: callable,
        target: QObject = None,
        title: str = None,
        description: str = None
    ) -> None:
        key_path = f"{self.__class__.__name__}.{name}"
        if key_path in self._shortcuts:
            raise PieException(f"Shortcut \"{name}/{shortcut}\" is already registered")

        shortcut_instance = QShortcut(QKeySequence(shortcut), self or target)
        shortcut_instance.activated.connect(triggered)
        setattr(self, key_path, shortcut_instance)
        self._shortcuts[key_path] = {
            "instance": shortcut_instance,
            "plugin_name": self.name,
            "title": title,
            "description": description,
        }

    def remove_shortcut(self, name: str) -> None:
        key_path = f"{self.__class__.__name__}.{name}"
        if key_path not in self._shortcuts:
            raise PieException(f"Shortcut \"{name}\" was not found")

        delattr(self, key_path)
        del self._shortcuts[key_path]

    def get_shortcuts(self) -> dict:
        return self._shortcuts


def main(parent: "QMainWindow", plugin_path: "Path"):
    return ShortcutManager(parent, plugin_path)

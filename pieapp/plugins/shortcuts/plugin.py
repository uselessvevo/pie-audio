from __feature__ import snake_case

from PySide6.QtCore import QObject
from PySide6.QtGui import QShortcut, QKeySequence

from pieapp.api.managers.registry import Registries
from pieapp.api.managers.structs import SysRegistry
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
        shortcut_name = f"{self.__class__.__name__}.{name}"
        if shortcut_name in self._shortcuts:
            raise PieException(f"Shortcut \"{name}/{shortcut}\" is already registered")

        shortcut_instance = QShortcut(QKeySequence(shortcut), target)
        shortcut_instance.activated.connect(triggered)
        setattr(self, shortcut_name, shortcut_instance)

        target_name = getattr(target, "name", target.__class__.__name__)
        payload = {
            "instance": shortcut_instance,
            "target_name": target_name,
            "title": title,
            "description": description,
        }

        Registries(SysRegistry.Shortcuts).add(shortcut_name, payload)

    def has_layout(self, name: str) -> bool:
        return Registries(SysRegistry.Shortcuts).has(name)

    def remove_shortcut(self, name: str) -> None:
        key_path = f"{self.__class__.__name__}.{name}"
        if key_path not in self._shortcuts:
            raise PieException(f"Shortcut \"{name}\" was not found")

        delattr(self, key_path)
        Registries(SysRegistry.Shortcuts).delete_shortcut()

    def get_shortcuts(self) -> dict:
        return Registries(SysRegistry.Shortcuts).get_shorcuts()


def main(parent: "QMainWindow", plugin_path: "Path"):
    return ShortcutManager(parent, plugin_path)

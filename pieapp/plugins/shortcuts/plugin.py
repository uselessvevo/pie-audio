from __feature__ import snake_case

from typing import Union

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QStyledItemDelegate

from pieapp.helpers.logger import logger
from pieapp.api.exceptions import PieException

from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.themes import ThemeProperties
from pieapp.api.models.shortcuts import ShortcutDict

from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_ready
from pieapp.api.plugins.decorators import on_plugin_shutdown

from pieapp.api.registries.registry import Registry
from pieapp.api.registries.models import SysRegistry
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin

from shortcuts.confpage import ShortcutConfigPage
from shortcuts.confpage import ShortcutBlankConfigPage


class ReadOnlyDelegate(QStyledItemDelegate):

    def create_editor(self, parent, option, index) -> None:
        return


class ShortcutManager(PiePlugin, ThemeAccessorMixin):
    name = SysPlugin.Shortcut
    requires = [SysPlugin.Preferences]

    @staticmethod
    def get_name() -> str:
        return translate("Shortcut")

    @staticmethod
    def get_description() -> str:
        return translate("Shortcut manager")

    def init(self) -> None:
        # TODO: Add shortcuts manifest file
        self._shortcut_registry = Registry(SysRegistry.Shortcuts)
        self._config_page_class = ShortcutBlankConfigPage

    def on_plugins_ready(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.update_config_page(self, SysPlugin.Shortcut, ShortcutConfigPage)

    # ConfigPage/Preferences plugin methods

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon(
            key="icons/app.svg",
            scope=self.name,
            color=self.get_theme_property(ThemeProperties.AppIconColor)
        )

    def get_config_page(self) -> Union[ShortcutBlankConfigPage, ShortcutConfigPage]:
        return self._config_page_class()

    @on_plugin_ready(plugin=SysPlugin.Preferences)
    def _on_preferences_available(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.register_config_page(self)

    @on_plugin_shutdown(plugin=SysPlugin.Preferences)
    def _on_preferences_teardown(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.deregister_config_page(self)

    # Public proxy methods for ShortcutsRegistry

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
        if self._shortcut_registry.contains(name):
            raise PieException(f"Shortcut \"{name}/{shortcut}\" is already registered")

        shortcut_instance = QShortcut(QKeySequence(shortcut), target)
        shortcut_instance.activated.connect(triggered)
        setattr(self, name, shortcut_instance)
        target_name: str = getattr(target, "name", target.__class__.__name__)
        self._shortcut_registry.add(name, shortcut_instance, target_name, title, shortcut, description, hidden)
        logger.debug(f"Shortcut {shortcut} was added in {target!s}")

    def remove_shortcut(self, shortcut_name: str) -> None:
        key_path = f"{self.__class__.__name__}.{shortcut_name}"
        delattr(self, key_path)
        self._shortcut_registry.delete_shortcut()

    def get_shortcuts(self) -> list[ShortcutDict]:
        return self._shortcut_registry.values()

    def contains_shortcut(self, name: str) -> bool:
        return self._shortcut_registry.contains(name)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return ShortcutManager(parent, plugin_path)

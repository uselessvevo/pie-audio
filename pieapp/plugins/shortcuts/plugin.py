from typing import Union

from PySide6.QtCore import QObject
from PySide6.QtGui import QShortcut, QKeySequence

from pieapp.api.registries.shortcuts.manager import Shortcuts
from pieapp.utils.logger import logger
from pieapp.api.exceptions import PieException

from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.themes import ThemeProperties
from pieapp.api.models.shortcuts import ShortcutDict

from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.plugins.decorators import on_plugin_shutdown

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin

from shortcuts.confpage import ShortcutConfigPage
from shortcuts.confpage import ShortcutBlankConfigPage


class ShortcutManager(PiePlugin, ThemeAccessorMixin):
    name = SysPlugin.Shortcut
    requires = [SysPlugin.Preferences]

    def get_name(self) -> str:
        return translate("Shortcuts")

    def get_description(self) -> str:
        return translate("Shortcut manager", scope=self.name)

    def init(self) -> None:
        # TODO: Add shortcuts manifest file
        self._config_page_class = ShortcutBlankConfigPage

    def on_plugins_ready(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.update_config_page(self, SysPlugin.Shortcut, ShortcutConfigPage)

    # ConfigPage/Preferences plugin methods

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon(
            key="icons/app.svg",
            scope=self.name,
            prop=ThemeProperties.AppIconColor
        )

    def get_config_page(self) -> Union[ShortcutBlankConfigPage, ShortcutConfigPage]:
        return self._config_page_class()

    @on_plugin_available(plugin=SysPlugin.Preferences)
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
        if Shortcuts.contains(name):
            raise PieException(f"Shortcut \"{name}/{shortcut}\" is already registered")

        shortcut_instance = QShortcut(QKeySequence(shortcut), target)
        shortcut_instance.activated.connect(triggered)
        setattr(self, name, shortcut_instance)
        target_name: str = getattr(target, "name", target.__class__.__name__)
        Shortcuts.add(name, shortcut_instance, target_name, title, shortcut, description, hidden)
        logger.debug(f"Shortcut {shortcut} was added in {target!s}")

    def remove_shortcut(self, shortcut_name: str) -> None:
        key_path = f"{self.__class__.__name__}.{shortcut_name}"
        delattr(self, key_path)
        Shortcuts.delete_shortcut()

    def get_shortcuts(self) -> list[ShortcutDict]:
        return Shortcuts.values()

    def contains_shortcut(self, name: str) -> bool:
        return Shortcuts.contains(name)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return ShortcutManager(parent, plugin_path)

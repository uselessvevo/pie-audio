from typing import Type

from pieapp.api.utils.logger import logger
from pieapp.api.exceptions import PieError

from pieapp.api.models.scopes import Scope
from pieapp.api.models.themes import IconName
from pieapp.api.models.menus import MainMenu
from pieapp.api.models.menus import MainMenuItem
from pieapp.api.models.plugins import SysPlugin

from pieapp.api.plugins import ConfigPage
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.plugins.mixins import WidgetsAccessorMixins

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.confpages.registry import ConfigPageRegistry

from preferences.widgets.mainwidget import PreferencesWidget


class Preferences(PiePlugin, ThemeAccessorMixin, WidgetsAccessorMixins):
    name = SysPlugin.Preferences
    requires = [SysPlugin.MainMenuBar]
    widget_class = PreferencesWidget

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon(
            key=IconName.App,
            scope=self.name
        )

    @staticmethod
    def get_title() -> str:
        return translate("Preferences")

    @staticmethod
    def get_description() -> str:
        return translate("Preferences widget")

    def init(self) -> None:
        widget = self.get_widget()
        widget.sig_accept.connect(self._on_pages_accept)
        widget.sig_cancel.connect(self._on_pages_cancel)
        widget.sig_apply.connect(self._on_pages_apply)

    # Public methods

    def register_config_page(self, config_page: Type[ConfigPage]) -> None:
        widget = self.get_widget()
        if issubclass(config_page, ConfigPage):
            config_page = config_page()
            ConfigPageRegistry.add(config_page.name, config_page)
            widget.register_config_page(config_page)

    def deregister_config_page(self, config_page: Type[ConfigPage]) -> None:
        widget = self.get_widget()
        if config_page.name in ConfigPageRegistry:
            ConfigPageRegistry.remove(config_page.name)
            widget.deregister_config_page(config_page)

    def update_config_page(self, page_name: str, new_page_class: Type[ConfigPage]) -> None:
        widget = self.get_widget()
        if page_name in ConfigPageRegistry:
            # TODO: Switch to registry signals?
            new_config_page = new_page_class()
            ConfigPageRegistry.update(page_name, new_config_page)
            widget.update_config_page(page_name, new_config_page)

    # Plugin and PluginsRegistry events

    def on_plugin_teardown(self, name: str) -> None:
        plugin = get_plugin(name)
        widget = self.get_widget()
        widget.deregister_config_page(plugin)

    # Private methods

    def _on_pages_accept(self) -> None:
        # TODO: Implement `apply_button_enabled` or `state_changed` flags/signals
        pages = ConfigPageRegistry.values()
        for page in pages:
            try:
                page.accept()
            except PieError as e:
                logger.debug(str(e))

        self.get_widget().close()

    def _on_pages_cancel(self) -> None:
        # TODO: Add changes tracker subscription
        pages = ConfigPageRegistry.values()
        for page in pages:
            try:
                page.cancel()
            except PieError as e:
                logger.debug(str(e))

        self.get_widget().close()

    def _on_pages_apply(self) -> None:
        pages = ConfigPageRegistry.values()
        for page in pages:
            try:
                page.accept()
            except PieError as e:
                logger.debug(str(e))

    @on_plugin_available(plugin=SysPlugin.MainMenuBar)
    def _on_menu_bar_available(self) -> None:
        self.add_menu_item(
            scope=Scope.Shared,
            menu=MainMenu.File,
            name="preferences",
            text=translate("Preferences"),
            triggered=self.get_widget().call,
            icon=self.get_plugin_icon(),
            after=MainMenuItem.OpenFiles
        )


def main(parent, plugin_path):
    return Preferences(parent, plugin_path)

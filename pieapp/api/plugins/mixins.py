from __future__ import annotations

from pieapp.api.globals import Global
from pieapp.api.models.scopes import Scope

from pieapp.api.registries.menus.mixins import MenuAccessorMixin
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin

from pieapp.api.registries.tabs.mixins import TabBarAccessorMixin
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.toolbars.mixins import ToolBarAccessorMixin
from pieapp.api.registries.toolbuttons.mixins import ToolButtonAccessorMixin
from pieapp.api.registries.shortcuts.mixins import ShortcutAccessorMixin


class CoreAccessorsMixin(
    ConfigAccessorMixin,
    ThemeAccessorMixin
):
    pass


class WidgetsAccessorMixins(
    ToolButtonAccessorMixin,
    ToolBarAccessorMixin,
    TabBarAccessorMixin,
    MenuAccessorMixin,
    ShortcutAccessorMixin,
):
    pass


class DialogWidgetMixin(ConfigAccessorMixin, WidgetsAccessorMixins):
    """
    Brand NEW "Essential and life improvement mixins for your plugin!"

    Contains:
        * Geometry methods
        * ConfigAccessorMixin methods
    """

    def get_default_geometry(self) -> list:
        main_window_geometry = self.parent().geometry()
        main_window_geometry = main_window_geometry.x(), main_window_geometry.y()
        return [*main_window_geometry, *Global.DEFAULT_WINDOW_SIZE]

    def save_widget_geometry(self) -> None:
        geometry = self.geometry()
        self.update_plugin_config("ui.geometry", Scope.User, (
            geometry.x(), geometry.y(), geometry.size().width(), geometry.size().height()
        ))
        self.save_plugin_config("ui", Scope.User, create=True)

    def restore_widget_geometry(self) -> None:
        self.set_geometry(*self.get_plugin_config("ui.geometry", Scope.User, self.get_default_geometry()))

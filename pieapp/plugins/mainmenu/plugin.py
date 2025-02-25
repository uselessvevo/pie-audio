from __feature__ import snake_case

from pieapp.api.models.indexes import Index
from pieapp.api.models.menus import MainMenu, MainMenuItem
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.scopes import Scope
from pieapp.api.models.themes import IconName

from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.registries.locales.helpers import translate

from pieapp.api.registries.menus.mixins import MenuAccessorMixin
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.utils.qt import get_main_window


class MainMenuBarPlugin(PiePlugin, MenuAccessorMixin, ThemeAccessorMixin):
    name = SysPlugin.MainMenuBar
    requires = [SysPlugin.Preferences]

    @staticmethod
    def get_title() -> str:
        return translate("Main menu bar")

    def init(self) -> None:
        self.menubar = self.add_menu_bar(SysPlugin.MainMenuBar)
        self.menubar.set_object_name(SysPlugin.MainMenuBar)

        file_menu = self.add_menu(
            scope=Scope.Shared,
            name=MainMenu.File,
            text=translate("File"),
        )
        help_menu = self.add_menu(
            scope=Scope.Shared,
            name=MainMenu.Help,
            text=translate("Help")
        )
        self.add_menu_item(
            scope=Scope.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.Exit,
            text=translate("Exit"),
            icon=self.get_svg_icon(IconName.Logout),
            triggered=self._parent.close,
            index=Index.End
        )

        self.menubar.add_pie_menu(file_menu)
        self.menubar.add_pie_menu(help_menu)

        get_main_window().set_menu_bar(self.menubar)

    def on_plugins_ready(self) -> None:
        # TODO: Use Global.SPAWN_DEFAULT_MENU_BAR?
        self.menubar.call()

    # @on_plugin_available(plugin=SysPlugin.Preferences)
    # def _on_preferences_available(self) -> None:
    #     preferences = get_plugin(SysPlugin.Preferences)
    #     preferences.register_config_page(self)
    #
    # @on_plugin_shutdown(plugin=SysPlugin.Preferences)
    # def _on_preferences_teardown(self) -> None:
    #     preferences = get_plugin(SysPlugin.Preferences)
    #     preferences.deregister_config_page(self)


def main(parent, plugin_path):
    return MainMenuBarPlugin(parent, plugin_path)


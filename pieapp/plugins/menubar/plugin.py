from __feature__ import snake_case

from pieapp.api.models.plugins import SysPlugin
from pieapp.api.registries.models import Scope

from pieapp.api.models.indexes import Index
from pieapp.api.models.menus import MainMenu
from pieapp.api.models.menus import MainMenuItem
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.menus.mixins import MenuAccessorMixin
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin


class MainMenuBar(PiePlugin, ThemeAccessorMixin, MenuAccessorMixin, ConfigAccessorMixin):
    name = SysPlugin.MainMenuBar

    def init(self) -> None:
        self._menubar = self.add_menu_bar(name=Scope.Shared)
        self._menubar.set_object_name("MainMenuBar")

        file_menu = self.add_menu(
            scope=Scope.Shared,
            parent=self._menubar,
            name=MainMenu.File,
            text=translate("File"),
        )
        help_menu = self.add_menu(
            scope=Scope.Shared,
            parent=self._menubar,
            name=MainMenu.Help,
            text=translate("Help")
        )
        self.add_menu_item(
            scope=Scope.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.Exit,
            text=translate("Exit"),
            icon=self.get_svg_icon("icons/logout.svg"),
            triggered=self._parent.close,
            index=Index.End
        )

        self._menubar.add_pie_menu(file_menu)
        self._menubar.add_pie_menu(help_menu)
        self._parent.set_menu_bar(self._menubar)

    def on_plugins_ready(self) -> None:
        self._menubar.call()


def main(parent: "QMainWindow", plugin_path: "Path"):
    return MainMenuBar(parent, plugin_path)


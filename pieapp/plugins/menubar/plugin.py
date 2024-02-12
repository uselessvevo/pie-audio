from pieapp.api.structs.plugins import Plugin
from pieapp.api.managers.structs import Section

from pieapp.widgets.menus import INDEX_END
from pieapp.api.structs.menus import MainMenu
from pieapp.api.structs.menus import MainMenuItem
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.managers.locales.helpers import translate
from pieapp.api.managers.menus.mixins import MenuAccessorMixin
from pieapp.api.managers.themes.mixins import ThemeAccessorMixin
from pieapp.api.managers.configs.mixins import ConfigAccessorMixin
from pieapp.api.managers.locales.mixins import LocalesAccessorMixin


class MainMenuBar(
    PiePlugin,
    ThemeAccessorMixin, MenuAccessorMixin,
    ConfigAccessorMixin, LocalesAccessorMixin,
):
    name = Plugin.MainMenuBar

    def init(self) -> None:
        menu_bar = self.add_menu_bar(
            name=Section.Shared,
        )
        menu_bar.set_object_name("MainMenuBar")

        file_menu = self.add_menu(
            section=Section.Shared,
            parent=menu_bar,
            name=MainMenu.File,
            text=translate("File"),
        )
        help_menu = self.add_menu(
            section=Section.Shared,
            parent=menu_bar,
            name=MainMenu.Help,
            text=translate("Help")
        )
        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.Exit,
            text=translate("Exit"),
            icon=self.get_svg_icon("icons/logout.svg"),
            triggered=self._parent.close,
            index=INDEX_END()
        )

        menu_bar.add_menu(file_menu)
        menu_bar.add_menu(help_menu)
        self._parent.set_menu_bar(menu_bar)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return MainMenuBar(parent, plugin_path)


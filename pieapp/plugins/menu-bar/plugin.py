from typing import Union

from pieapp.structs.menus import MainMenu, MainMenuItem
from pieapp.structs.plugins import Plugin
from piekit.managers.menus.mixins import MenuAccessorMixin
from piekit.plugins.plugins import PiePlugin

from piekit.managers.structs import Section
from piekit.managers.themes.mixins import ThemeAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.widgets.menus import INDEX_END


class MainMenuBar(
    PiePlugin,
    ThemeAccessorMixin, MenuAccessorMixin,
    ConfigAccessorMixin, LocalesAccessorMixin,
):
    name = Plugin.MenuBar

    def init(self) -> None:
        self._menu_bar = self.add_menu_bar(
            name=Section.Shared,
        )
        self._menu_bar.set_object_name("MainMenuBar")

        self._file_menu = self.add_menu(
            section=Section.Shared,
            parent=self._menu_bar,
            name=MainMenu.File,
            text=self.translate("File"),
        )
        self._help_menu = self.add_menu(
            section=Section.Shared,
            parent=self._menu_bar,
            name=MainMenu.Help,
            text=self.translate("Help")
        )
        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.Exit,
            text=self.translate("Exit"),
            icon=self.get_svg_icon("icons/logout.svg"),
            triggered=self._parent.close,
            index=INDEX_END()
        )

        self._menu_bar.add_menu(self._file_menu)
        self._menu_bar.add_menu(self._help_menu)
        self._parent.set_menu_bar(self._menu_bar)


def main(parent: "QMainWindow", plugin_path: "Path") -> Union[PiePlugin, None]:
    return MainMenuBar(parent, plugin_path)

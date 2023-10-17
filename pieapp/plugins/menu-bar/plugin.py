from typing import Union

from pieapp.structs.menus import MainMenu, MainMenuItem
from pieapp.structs.plugins import Plugin
from piekit.managers.menus.mixins import MenuAccessorMixin
from piekit.plugins.plugins import PiePlugin

from piekit.managers.structs import Section
from piekit.managers.icons.mixins import IconAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.widgets.menus import INDEX_END


class MainMenuBar(
    PiePlugin,
    IconAccessorMixin, MenuAccessorMixin,
    ConfigAccessorMixin, LocalesAccessorMixin,
):
    name = Plugin.MenuBar

    def init(self) -> None:
        self._menu_bar = self.add_menu_bar(
            name=Section.Shared,
        )

        self._file_menu = self.add_menu(
            section=Section.Shared,
            parent=self._menu_bar,
            name=MainMenu.File,
            text=self.get_translation("File"),
        )
        self._help_menu = self.add_menu(
            section=Section.Shared,
            parent=self._menu_bar,
            name=MainMenu.Help,
            text=self.get_translation("Help")
        )
        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.Exit,
            text=self.get_translation("Exit"),
            icon=self.get_svg_icon("logout.svg"),
            triggered=self._parent.close,
            index=INDEX_END()
        )

        self._menu_bar.add_menu(self._file_menu)
        self._menu_bar.add_menu(self._help_menu)
        self._parent.set_menu_bar(self._menu_bar)


def main(parent: "QMainWindow", plugin_path: "Path") -> Union[PiePlugin, None]:
    return MainMenuBar(parent, plugin_path)

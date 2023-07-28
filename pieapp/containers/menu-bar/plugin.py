from typing import Union

from pieapp.structs.menus import MainMenu
from pieapp.structs.containers import Container
from piekit.managers.menus.mixins import MenuAccessor
from piekit.plugins.plugins import PiePlugin

from piekit.managers.structs import Section
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class MenuBar(
    PiePlugin,
    AssetsAccessor, MenuAccessor,
    ConfigAccessor, LocalesAccessor,
):
    name = Container.MenuBar

    def init(self) -> None:
        self.menu_bar = self.add_menu_bar(
            name=Section.Shared,
        )

        self.file_menu = self.add_menu(
            section=Section.Shared,
            parent=self.menu_bar,
            name=MainMenu.File,
            text=self.get_translation("File"),
        )
        self.help_menu = self.add_menu(
            section=Section.Shared,
            parent=self.menu_bar,
            name=MainMenu.Help,
            text=self.get_translation("Help")
        )

        self.menu_bar.add_menu(self.file_menu)
        self.menu_bar.add_menu(self.help_menu)
        self._parent.set_menu_bar(self.menu_bar)


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    return MenuBar(*args, **kwargs)

import typing

from pieapp.structs.menus import Menus
from pieapp.structs.containers import Containers
from piekit.managers.menus.mixins import MenuAccessor
from piekit.plugins.plugins import PiePlugin

from piekit.managers.structs import Sections
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class MenuBar(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    MenuAccessor,
):
    name = Containers.MenuBar

    def init(self) -> None:
        self.menu_bar = self.add_menu_bar(
            name=Sections.Shared,
        )

        self.file_menu = self.add_menu(
            section=Sections.Shared,
            parent=self.menu_bar,
            name=Menus.File,
            text=self.get_translation("File"),
        )
        self.help_menu = self.add_menu(
            section=Sections.Shared,
            parent=self.menu_bar,
            name=Menus.Help,
            text=self.get_translation("Help")
        )

        self.menu_bar.add_menu(self.file_menu)
        self.menu_bar.add_menu(self.help_menu)
        self._parent.set_menu_bar(self.menu_bar)


def main(*args, **kwargs) -> typing.Any:
    return MenuBar(*args, **kwargs)

from typing import Union

from pieapp.structs.menus import MainMenu
from pieapp.structs.containers import Container
from piekit.managers.menus.mixins import MenuAccessorMixin
from piekit.plugins.plugins import PiePlugin

from piekit.managers.structs import Section
from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin


class MainMenuBar(
    PiePlugin,
    AssetsAccessorMixin, MenuAccessorMixin,
    ConfigAccessorMixin, LocalesAccessorMixin,
):
    name = Container.MenuBar

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

        self._menu_bar.add_menu(self._file_menu)
        self._menu_bar.add_menu(self._help_menu)
        self._parent.set_menu_bar(self._menu_bar)


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    return MainMenuBar(*args, **kwargs)

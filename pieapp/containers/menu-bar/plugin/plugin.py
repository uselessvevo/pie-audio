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
        self.menuBar = self.addMenuBar(
            name=Sections.Shared,
        )

        self.fileMenu = self.addMenu(
            section=Sections.Shared,
            parent=self.menuBar,
            name=Menus.File,
            text=self.getTranslation("File"),
        )
        self.helpMenu = self.addMenu(
            section=Sections.Shared,
            parent=self.menuBar,
            name=Menus.Help,
            text=self.getTranslation("Help")
        )

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.helpMenu)
        self.parent().setMenuBar(self.menuBar)


def main(*args, **kwargs) -> typing.Any:
    return MenuBar(*args, **kwargs)

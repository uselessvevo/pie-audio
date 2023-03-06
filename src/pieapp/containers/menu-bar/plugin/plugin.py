import typing

from PyQt5.QtWidgets import QMenuBar

from pieapp.structs.containers import Containers
from pieapp.structs.menus import Menus
from piekit.managers.menus.mixins import MenuAccessor
from piekit.plugins.base import PiePlugin

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
        self._menuBar = QMenuBar()

        self.fileMenu = self.addMenu(
            section=Sections.Shared,
            parent=self._menuBar,
            name=Menus.File,
            text=self.getTranslation("File"),
        )

        self.addMenuItem(
            section=Sections.Shared,
            menu=self.fileMenu.name,
            name="openFiles",
            text=self.getTranslation("Open file"),
            icon=self.getAssetIcon("open-file.png")
        )

        self.addMenuItem(
            section=Sections.Shared,
            menu=self.fileMenu.name,
            name="exit",
            text=self.getTranslation("Exit"),
            icon=self.getAssetIcon("exit.png"),
            triggered=self.parent().close
        )

        # Help menu
        self.helpMenu = self.addMenu(
            section=Sections.Shared,
            parent=self._menuBar,
            name=Menus.Help,
            text=self.getTranslation("Help")
        )

        self._menuBar.addMenu(self.fileMenu)
        self._menuBar.addMenu(self.helpMenu)

        self.parent().setMenuBar(self._menuBar)


def main(*args, **kwargs) -> typing.Any:
    return MenuBar(*args, **kwargs)

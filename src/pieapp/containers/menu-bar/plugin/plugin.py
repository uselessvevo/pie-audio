import typing

from PyQt5.QtWidgets import QMenuBar

from piekit.plugins.mixins import MenuMixin
from piekit.plugins.base import PiePlugin

from piekit.managers.types import Sections
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class MenuBar(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    MenuMixin,
):
    name = "menu-bar"
    requires = ["about-app"]

    def init(self) -> None:
        self._menuBar = QMenuBar()

        self.fileMenu = self.addMenu(
            section=Sections.Shared,
            parent=self._menuBar,
            name="file",
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
            name="settings",
            text=self.getTranslation("Settings"),
            icon=self.getAssetIcon("settings.png")
        )

        exitAction = self.addMenuItem(
            section=Sections.Shared,
            menu=self.fileMenu.name,
            name="exit",
            text=self.getTranslation("Exit"),
            icon=self.getAssetIcon("exit.png")
        )
        exitAction.triggered.connect(self.parent().close)

        # About menu
        self.helpMenu = self.addMenu(
            section=Sections.Shared,
            parent=self._menuBar,
            name="help",
            text=self.getTranslation("Help")
        )

        self._menuBar.addMenu(self.fileMenu)
        self._menuBar.addMenu(self.helpMenu)

        self.parent().setMenuBar(self._menuBar)


def main(*args, **kwargs) -> typing.Any:
    return MenuBar(*args, **kwargs)

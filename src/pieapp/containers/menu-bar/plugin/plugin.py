from functools import partial

from PyQt5.QtWidgets import QMenuBar

from piekit.containers.containers import PieContainer
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.objects.decorators import onObjectAvailable
from piekit.managers.types import SysManagers
from piekit.managers.registry import Managers
from piekit.objects.mixins import MenuMixin


class MenuBar(
    PieContainer,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    MenuMixin,
):
    name = "menu-bar"
    requires = ["about-app"]

    def init(self) -> None:
        self._menuBar = QMenuBar()

        fileMenu = self.addMenu(
            parent=self._menuBar,
            name="file",
            text=self.getTranslation("File"),
        )

        self.addMenuItem(
            menu=fileMenu.name,
            name="openFiles",
            text=self.getTranslation("Open file"),
            icon=self.getAssetIcon("open-file.png")
        )

        self.addMenuItem(
            menu=fileMenu.name,
            name="settings",
            text=self.getTranslation("Settings"),
            icon=self.getAssetIcon("settings.png")
        )

        exitAction = self.addMenuItem(
            menu=fileMenu.name,
            name="exit",
            text=self.getTranslation("Exit"),
            icon=self.getAssetIcon("exit.png")
        )
        exitAction.triggered.connect(self.parent().close)

        # About menu
        etcMenu = self.addMenu(
            parent=self._menuBar,
            name="etc",
            text=self.getTranslation("Etc")
        )

        self._aboutAction = self.addMenuItem(
            menu=etcMenu.name,
            name="about",
            text=self.getTranslation("About"),
            icon=self.getAssetIcon("help.png")
        )
        self._aboutAction.setDisabled(True)
        self._aboutAction.triggered.connect(self._showAboutApp)

        self._menuBar.addMenu(fileMenu)
        self._menuBar.addMenu(etcMenu)

        self.parent().setMenuBar(self._menuBar)

    @onObjectAvailable(target="about-app")
    def onAboutAppAvailable(self) -> None:
        self._aboutAction.setDisabled(False)

    @staticmethod
    def _showAboutApp() -> None:
        Managers(SysManagers.Objects)("about-app").render()

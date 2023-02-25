from PyQt5.QtWidgets import QMenuBar

from piekit.containers.containers import PieContainer
from piekit.objects.mixins import MenuMixin
from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers, Sections

from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


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
        self.etcMenu = self.addMenu(
            section=Sections.Shared,
            parent=self._menuBar,
            name="etc",
            text=self.getTranslation("Etc")
        )

        self._menuBar.addMenu(self.fileMenu)
        self._menuBar.addMenu(self.etcMenu)

        self.parent().setMenuBar(self._menuBar)

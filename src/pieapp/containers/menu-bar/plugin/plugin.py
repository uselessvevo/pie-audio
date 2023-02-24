from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

from piekit.containers.containers import PieContainer
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.types import SysManagers
from piekit.objects.mixins import MenuMixin


class MenuBar(
    PieContainer,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    MenuMixin,
):
    name = SysManagers.Menus

    def init(self) -> None:
        menuBar = QMenuBar()

        fileMenu = self.addMenu(
            parent=menuBar,
            name="file",
            text=self.getTranslation("File"),
            # icon=self.getAssetIcon("open-file.png")
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

        menuBar.addMenu(fileMenu)

        self.parent().setMenuBar(menuBar)

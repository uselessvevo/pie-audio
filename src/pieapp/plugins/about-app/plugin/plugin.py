import typing

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from pieapp.types import Containers
from piekit.plugins.base import PiePlugin
from piekit.plugins.mixins import MenuAccessor

from piekit.managers.types import Sections
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.plugins.decorators import onPluginAvailable


class About(
    PiePlugin,
    MenuAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "about-app"
    requires = ["menu-bar"]

    def init(self) -> None:
        self.widget = QWidget()
        self.widget.setWindowTitle(self.getTranslation("About app"))

        pixmap = QPixmap()
        pixmap.load(self.getAsset("cloud.png"))

        appIcon = QLabel(self.widget)
        appIcon.setPixmap(pixmap)

        self.widget.setWindowIcon(self.getAssetIcon("plugin.png"))
        self.widget.resize(400, 300)

    @onPluginAvailable(target=Containers.MenuBar)
    def onMenuBarAvailable(self) -> None:
        self.getMenu(Sections.Shared, "help").addMenuItem(
            name="about",
            text=self.getTranslation("About"),
            icon=self.getAssetIcon("help.png")
        ).triggered.connect(self.widget.show)


def main(*args, **kwargs) -> typing.Any:
    return About(*args, **kwargs)

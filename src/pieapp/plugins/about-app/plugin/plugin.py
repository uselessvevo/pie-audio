from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton

from piekit.managers.objects.decorators import onObjectAvailable
from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers, Sections
from piekit.objects.mixins import MenuMixin
from piekit.plugins.base import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class AboutApp(
    PiePlugin,
    MenuMixin,
    ConfigAccessor,
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

    @onObjectAvailable(target="menu-bar")
    def onMenuBarAvailable(self) -> None:
        menu = self.getMenu(Sections.Shared, "help")
        menu.addMenuItem(
            name="about",
            text=self.getTranslation("About"),
            icon=self.getAssetIcon("help.png")
        )
        menu.triggered.connect(self.render)

    def render(self) -> None:
        self.widget.show()

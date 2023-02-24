from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton

from piekit.plugins.base import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class AboutApp(
    PiePlugin,
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

        self.widget.resize(400, 300)

    def render(self) -> None:
        self.widget.show()

import typing

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton, QDialog

from piekit.plugins.base import PiePlugin
from pieapp.structs.plugins import Plugins
from pieapp.structs.containers import Containers
from piekit.managers.menus.mixins import MenuAccessor

from piekit.system.loader import Config
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.plugins.decorators import onPluginAvailable


class About(
    PiePlugin,
    MenuAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = Plugins.About
    requires = [Containers.MenuBar]

    def init(self) -> None:
        self.dialog = QDialog(self.parent())
        self.dialog.setWindowTitle(self.getTranslation("About"))

        okButton = QPushButton(self.getTranslation("Ok"))
        okButton.clicked.connect(self.dialog.close)

        pixmap = QPixmap()
        pixmap.load(self.getAsset("cloud.png"))

        iconLabel = QLabel()
        iconLabel.setPixmap(pixmap)

        descriptionLabel = QLabel()
        descriptionLabel.setText("Pie Audio • Audio Converter ({})".format(
            Config.PIEAPP_VERSION
        ))

        githubLinkLabel = QLabel()
        githubLinkLabel.setOpenExternalLinks(True)
        githubLinkLabel.setText("<a href='https://github.com/uselessvevo/pie-audio/'>Project URL</a>")

        gridLayout = QGridLayout()
        gridLayout.addWidget(iconLabel, 0, 0, alignment=Qt.AlignHCenter)
        gridLayout.addWidget(descriptionLabel, 1, 0, alignment=Qt.AlignHCenter)
        gridLayout.addWidget(githubLinkLabel, 2, 0, alignment=Qt.AlignHCenter)
        gridLayout.addWidget(okButton, 3, 0, alignment=Qt.AlignRight)

        self.dialog.setLayout(gridLayout)
        self.dialog.setWindowIcon(self.getAssetIcon("help.png"))
        self.dialog.resize(400, 300)

    @onPluginAvailable(target=Containers.MenuBar)
    def onMenuBarAvailable(self) -> None:
        self.addMenuItem(
            menu="help",
            name="about",
            text=self.getTranslation("About"),
            triggered=self.dialog.show,
            icon=self.getAssetIcon("help.png")
        )


def main(*args, **kwargs) -> typing.Any:
    return About(*args, **kwargs)

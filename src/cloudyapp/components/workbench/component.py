from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QToolBar

from cloudykit.managers.plugins.decorators import onPluginAvailable
from cloudykit.system import SharedSection
from cloudykit.components.base import BaseComponent


class Workbench(QToolBar, BaseComponent):

    def __init__(self, parent: "MainWindow") -> None:
        super().__init__(parent)

    def call(self) -> None:
        self.setMovable(False)
        self.setIconSize(QtCore.QSize(30, 30))
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setOrientation(Qt.Horizontal)
        self.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum
        ))

        settings = QtWidgets.QToolButton()
        settings.setToolTip(self.getTranslation("Settings"))
        settings.setIcon(QtGui.QIcon(self.getAsset("settings.svg")))
        settings.setToolButtonStyle(Qt.ToolButtonIconOnly)

        spacer = QtWidgets.QWidget()
        spacer.setObjectName("spacer")
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self.addWidget(spacer)
        self.addWidget(settings)

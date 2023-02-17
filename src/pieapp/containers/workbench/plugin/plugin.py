from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QToolBar

from piekit.plugins.base import BasePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class Workbench(
    BasePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "workbench"

    def init(self) -> None:
        self.toolBar = QToolBar(self._parent)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(30, 30))
        self.toolBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBar.setOrientation(Qt.Vertical)
        self.toolBar.setSizePolicy(QtWidgets.QSizePolicy(
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

        self.toolBar.addWidget(spacer)
        self.toolBar.addWidget(settings)
        self._parent.addToolBar(Qt.LeftToolBarArea, self.toolBar)

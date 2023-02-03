from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from cloudykit.components.base import BaseComponent


class Workbench(QtWidgets.QToolBar, BaseComponent):

    def __init__(self, parent):
        super().__init__(parent)

    def mount(self) -> None:
        self.setMovable(False)
        self.setIconSize(QtCore.QSize(30, 30))
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setOrientation(Qt.Horizontal)
        self.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum
        ))

        openFolder = QtWidgets.QToolButton()
        openFolder.setToolTip(self.registry.locales("shared", "Open folder"))
        openFolder.setIcon(QtGui.QIcon(self.registry.assets("shared", "folder-open.svg")))
        openFolder.setToolButtonStyle(Qt.ToolButtonIconOnly)

        search = QtWidgets.QToolButton()
        search.setToolTip(self.registry.locales("shared", "Search"))
        search.setIcon(QtGui.QIcon(self.registry.assets("shared", "search.svg")))
        search.setToolButtonStyle(Qt.ToolButtonIconOnly)

        settings = QtWidgets.QToolButton()
        settings.setToolTip(self.registry.locales("shared", "Settings"))
        settings.setIcon(QtGui.QIcon(self.registry.assets("shared", "settings.svg")))
        settings.setToolButtonStyle(Qt.ToolButtonIconOnly)

        runProcess = QtWidgets.QToolButton()
        runProcess.setToolTip(self.registry.locales("shared", "Run"))
        runProcess.setIcon(QtGui.QIcon(self.registry.assets("shared/icons/start.svg")))
        runProcess.setToolButtonStyle(Qt.ToolButtonIconOnly)

        spacer = QtWidgets.QWidget()
        spacer.setObjectName("spacer")
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self.addWidget(openFolder)
        self.addWidget(search)
        self.addWidget(spacer)
        self.addWidget(settings)

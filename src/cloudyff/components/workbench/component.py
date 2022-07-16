from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from cloudykit.system.manager import System
from cloudykit.abstracts.component import IComponent


class Workbench(IComponent, QtWidgets.QToolBar):
    name = 'cloudyff_workbench'

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self._parent = parent
        self.assets = System.assets
        self.trans = System.locales

    def init(self):
        self.setMovable(False)
        self.setIconSize(QtCore.QSize(30, 30))
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setOrientation(Qt.Vertical)
        self.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Maximum
        ))

        openFolder = QtWidgets.QToolButton()
        openFolder.setToolTip(self.trans('Open folder'))
        openFolder.setIcon(QtGui.QIcon(self.assets('shared/icons/folder-open.svg')))
        openFolder.setToolButtonStyle(Qt.ToolButtonIconOnly)

        search = QtWidgets.QToolButton()
        search.setToolTip(self.trans('Search'))
        search.setIcon(QtGui.QIcon(self.assets('shared/icons/search.svg')))
        search.setToolButtonStyle(Qt.ToolButtonIconOnly)

        settings = QtWidgets.QToolButton()
        settings.setToolTip(self.trans('Settings'))
        settings.setIcon(QtGui.QIcon(self.assets('shared/icons/settings.svg')))
        settings.setToolButtonStyle(Qt.ToolButtonIconOnly)

        runProcess = QtWidgets.QToolButton()
        runProcess.setToolTip(self.trans('Run process'))
        runProcess.setIcon(QtGui.QIcon(self.assets('shared/icons/start.svg')))
        runProcess.setToolButtonStyle(Qt.ToolButtonIconOnly)

        spacer = QtWidgets.QWidget()
        spacer.setObjectName('spacer')
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self.runConsole = QtWidgets.QToolButton()
        self.runConsole.setToolTip(self.trans('Open console'))
        self.runConsole.setIcon(QtGui.QIcon(self.assets('shared/icons/bug.svg')))
        self.runConsole.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Pack all default actions
        self.addWidget(openFolder)
        self.addWidget(search)
        self.addWidget(runProcess)
        self.addWidget(spacer)
        self.addWidget(self.runConsole)
        self.addWidget(settings)

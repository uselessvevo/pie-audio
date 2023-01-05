from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from cloudykit.objects.component import BaseComponent


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
        openFolder.setToolTip(self.registry.locales("Shared.OpenFolder"))
        openFolder.setIcon(QtGui.QIcon(self.registry.assets("shared/icons/folder-open.svg")))
        openFolder.setToolButtonStyle(Qt.ToolButtonIconOnly)

        search = QtWidgets.QToolButton()
        search.setToolTip(self.registry.locales("Shared.Search"))
        search.setIcon(QtGui.QIcon(self.registry.assets("shared/icons/search.svg")))
        search.setToolButtonStyle(Qt.ToolButtonIconOnly)

        settings = QtWidgets.QToolButton()
        settings.setToolTip(self.registry.locales("Shared.Settings"))
        settings.setIcon(QtGui.QIcon(self.registry.assets("shared/icons/settings.svg")))
        settings.setToolButtonStyle(Qt.ToolButtonIconOnly)

        runProcess = QtWidgets.QToolButton()
        runProcess.setToolTip(self.registry.locales("Shared.RunProcess"))
        runProcess.setIcon(QtGui.QIcon(self.registry.assets("shared/icons/start.svg")))
        runProcess.setToolButtonStyle(Qt.ToolButtonIconOnly)

        spacer = QtWidgets.QWidget()
        spacer.setObjectName("spacer")
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self.runConsole = QtWidgets.QToolButton()
        self.runConsole.setToolTip(self.registry.locales("Shared.runConsole"))
        self.runConsole.setIcon(QtGui.QIcon(self.registry.assets("shared/icons/bug.svg")))
        self.runConsole.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Pack all default actions
        self.addWidget(openFolder)
        self.addWidget(search)
        self.addWidget(spacer)
        self.addWidget(settings)

    def register(self, toolButton: QtWidgets.QToolButton) -> None:
        raise NotImplementedError("Method `register` must be implemented")

    def unregister(self):
        raise NotImplementedError("Method `unregister` must be implemented")

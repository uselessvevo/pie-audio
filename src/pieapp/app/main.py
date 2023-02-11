import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QIcon

from piekit.managers.registry import Managers
from piekit.structs.managers import SysManagersEnum
from piekit.utils.core import getApplication
from piekit.mainwindow.main import MainWindow
from piekit.managers.assets.utils import getTheme, getPalette


class PieAudioApp(MainWindow):
    section = "shared"
    version = (0, 1, 0)

    signalPluginsReady = pyqtSignal()
    signalComponentsReady = pyqtSignal()
    signalComponentsLoading = pyqtSignal()

    def init(self) -> None:
        self.setWindowTitle("Pie Audio • Audio Converter ({})".format(
            ".".join(str(i) for i in self.version)
        ))
        self.setMinimumSize(720, 480)
        self.resize(*self.getConfig("ui.winsize", (720, 480)))
        self.setWindowIcon(QIcon(self.getAsset("bug.svg")))

    def prepare(self):
        self.prepareBaseSignals()
        self.prepareStatusBar()
        self.prepareMainLayout()
        self.preparePlugins()

    def prepareMainLayout(self):
        self.mainHBox = QtWidgets.QHBoxLayout()
        self.toolBarHBox = QtWidgets.QHBoxLayout()
        self.workbenchVBox = QtWidgets.QVBoxLayout()
        self.treeViewVBox = QtWidgets.QVBoxLayout()
        self.editorHBox = QtWidgets.QHBoxLayout()

        self.mainHBox.addLayout(self.workbenchVBox)
        self.mainHBox.addLayout(self.treeViewVBox)
        self.mainHBox.addLayout(self.editorHBox)
        self.setLayout(self.mainHBox)

        self.mainHBox.setContentsMargins(0, 0, 0, 0)
        self.mainHBox.setSpacing(20)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.mainHBox)
        self.setCentralWidget(widget)

        self.signalComponentsLoading.emit()

    def prepareStatusBar(self):
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.insertPermanentWidget(0, QtWidgets.QWidget())
        self.setStatusBar(self.statusBar)

    # Plugin method and signals

    def preparePlugins(self) -> None:
        """ Prepare all (or selected) plugins """
        Managers.get(SysManagersEnum.Plugins).mount(self)
        self.signalPluginsReady.emit()

    @pyqtSlot(str)
    def pluginLoading(self, name: str) -> None:
        self.statusBar.showMessage(self.getTranslation("Plugin {} is loading".format(name)))

    @pyqtSlot(str)
    def pluginReady(self, name: str) -> None:
        self.statusBar.showMessage(self.getTranslation("Plugin {} is ready".format(name)))

    @pyqtSlot(str)
    def pluginReloading(self, name: str) -> None:
        self.statusBar.showMessage(self.getTranslation("Plugin {} reloading".format(name)))

    def notifyPluginsReady(self):
        self.statusBar.showMessage(self.getTranslation("Plugins are ready"))


def main() -> None:
    """ Main entrypoint """
    app = getApplication(sys.argv)
    theme = Managers.get(SysManagersEnum.Assets).theme
    if theme:
        app.setStyleSheet(getTheme(theme))
        palette = getPalette(theme)
        if palette:
            app.setPalette(palette)

    cloudy_app = PieAudioApp()
    cloudy_app.prepare()
    cloudy_app.init()
    cloudy_app.show()

    sys.exit(app.exec_())

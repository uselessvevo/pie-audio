import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from cloudyui.utils.core import getApplication
from cloudykit.objects.mainwindow import MainWindow


class CloudyApp(MainWindow):

    signalComponentsLoading = pyqtSignal()
    signalPluginsReady = pyqtSignal()
    signalComponentsReady = pyqtSignal()

    def mount(self):
        self.setMinimumSize(self.registry.configs.get("ui.minsize") or 720, 480)
        if isinstance(self.registry.configs.get("ui.maxsize"), tuple):
            self.setMaximumSize(self.registry.configs.get("ui.maxsize"))

        self.setWindowTitle(f"CloudyFF • Audio/Video Converter")
        self.prepareBaseSignals()
        self.prepareSignals()
        self.prepareStatusBar()
        self.prepareMainLayout()
        self.preparePlugins()

    def prepareSignals(self):
        self.signalComponentsLoading.connect(self.prepareComponents)
        self.signalPluginsReady.connect(self.notifyPluginsReady)
        self.signalComponentsReady.connect(self.notifyComponentsReady)

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

    def prepareComponents(self):
        """ Load all components """
        self.signalComponentsReady.emit()

    def reloadComponents(self):
        """ Reload all components """
        self.signalComponentsReady.emit()

    # Plugin method and signals

    def preparePlugins(self) -> None:
        """ Prepare all (or selected) plugins """
        self.registry.plugins.mount(self)
        self.signalPluginsReady.emit()

    @pyqtSlot(str)
    def pluginLoading(self, name: str) -> None:
        self.statusBar.showMessage(self.registry.locales("Plugin {} is loading".format(name)))

    @pyqtSlot(str)
    def pluginReady(self, name: str) -> None:
        self.statusBar.showMessage(self.registry.locales("Plugin {} is ready".format(name)))

    @pyqtSlot(str)
    def pluginReloading(self, name: str) -> None:
        self.statusBar.showMessage(self.registry.locales("Plugin {} reloading".format(name)))

    def notifyPluginsReady(self):
        self.statusBar.showMessage(self.registry.locales("Plugins are ready"))

    def notifyComponentsReady(self):
        self.statusBar.showMessage(self.registry.locales("Components are ready"))


def main() -> None:
    """ Main entrypoint """
    app = getApplication(sys.argv)

    cloudy_app = CloudyApp()
    cloudy_app.mount()
    cloudy_app.show()

    sys.exit(app.exec_())

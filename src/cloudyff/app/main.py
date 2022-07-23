import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from cloudykit.managers.system.manager import System
from cloudykit.utils.modules import is_debug
from cloudyui.base.splashcreen import createSplashScreen
from cloudykit.managers.components.manager import ComponentsManager

from cloudykit.managers.plugins.manager import PluginsManager
from cloudykit.utils.logger import DummyLogger
from utils.qt import getQtApp

logger = DummyLogger('CloudyApp')


class CloudyApp(QtWidgets.QMainWindow):

    signalLayoutReady = pyqtSignal()
    signalPluginsReady = pyqtSignal()
    signalComponentsReady = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.pluginsManager = PluginsManager()
        self.componentsManager = ComponentsManager()

        self.setMinimumSize(720, 480)

        self.prepareSignals()
        self.prepareStatusBar()
        self.prepareMainLayout()

    def prepareSignals(self):
        self.signalLayoutReady.connect(self.prepareComponents)
        self.signalPluginsReady.connect(self.notifyPluginsReady)
        self.signalComponentsReady.connect(self.preparePlugins)

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

        self.signalLayoutReady.emit()

    def notifyPluginsReady(self):
        self.statusBar.showMessage(System.locales('Plugins are ready'))

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

    def preparePlugins(self) -> None:
        """ Prepare all (or selected) plugins """
        self.pluginsManager.mount(self)
        self.signalPluginsReady.emit()


def main() -> None:
    """ Main entrypoint """
    # Define main Qt Application
    app = getQtApp(sys.argv)

    # Define splash screen widget
    splash = None
    if not is_debug() and (System.root / 'branding/splash.svg').exists():
        splash = createSplashScreen(
            path=System.root / 'branding/splash.svg',
            width=720,
            height=480,
            project_name='CloudyFF'
        )
        splash.show()

    # Define main app instance
    cloudy_app = CloudyApp()
    cloudy_app.show()

    if splash:
        splash.close()
    sys.exit(app.exec_())

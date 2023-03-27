from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout

from pieapp.structs.containers import Containers
from piekit.plugins.helpers import getPlugin
from piekit.system import Config
from piekit.mainwindow.main import MainWindow
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections
from piekit.managers.configs.mixins import ConfigAccessor


class PieAudioApp(MainWindow, ConfigAccessor):
    section = Sections.Shared
    signalPluginsReady = pyqtSignal()

    def init(self) -> None:
        self.setWindowTitle("Pie Audio • Audio Converter ({})".format(
            Config.PIEAPP_VERSION
        ))
        self.setMinimumSize(720, 480)
        self.resize(*self.getConfig("ui.winsize", (900, 560), Sections.User))
        self.setWindowIcon(QIcon(self.getAsset("cloud.png")))

    def prepareSignals(self) -> None:
        self.signalPluginsReady.connect(self.notifyPluginReady)

    def prepare(self):
        self.prepareBaseSignals()
        self.prepareSignals()
        self.prepareMainLayout()
        self.prepareCentralDefaultWidget()
        self.preparePlugins()

    def prepareMainLayout(self) -> None:
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

    def prepareCentralDefaultWidget(self):
        widget = QtWidgets.QLabel()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

    # Plugin method and signals

    def preparePlugins(self) -> None:
        """ Prepare all (or selected) Plugins """
        Managers(SysManagers.Plugins).mount(self)
        self.signalPluginsReady.emit()

    def notifyPluginReady(self):
        getPlugin(Containers.StatusBar).showMessage(self.getTranslation("Plugins are ready"))

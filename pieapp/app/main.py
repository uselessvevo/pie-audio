from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGridLayout

from piekit.config import Config
from pieapp.structs.containers import Containers
from piekit.plugins.utils import getPlugin
from piekit.mainwindow.main import MainWindow
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections
from piekit.managers.configs.mixins import ConfigAccessor


class PieAudioApp(MainWindow, ConfigAccessor):
    name = Config.PIEAPP_NAME
    section = Sections.Shared
    signalPluginsReady = Signal()

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
        self.prepareWorkbenchLayout()
        self.prepareTableLayout()
        self.prepareCentralDefaultWidget()
        self.preparePlugins()

    def prepareMainLayout(self) -> None:
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

    def prepareWorkbenchLayout(self) -> None:
        self.workbenchLayout = QGridLayout()
        self.mainLayout.addLayout(self.workbenchLayout, 0, 0)

    def prepareTableLayout(self) -> None:
        self.tableLayout = QGridLayout()
        self.mainLayout.addLayout(self.tableLayout, 1, 0)

    def prepareCentralDefaultWidget(self):
        widget = QtWidgets.QLabel()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

    # Plugin method and signals

    def preparePlugins(self) -> None:
        """ Prepare all (or selected) Plugins """
        Managers(SysManagers.Plugins).init(self)
        self.signalPluginsReady.emit()

    def notifyPluginReady(self):
        getPlugin(Containers.StatusBar).showMessage(self.getTranslation("Plugins are ready"))

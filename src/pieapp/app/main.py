from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

from pieapp.types import Containers
from piekit.system.loader import Config
from piekit.mainwindow.main import MainWindow
from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers, Sections
from piekit.managers.configs.mixins import ConfigAccessor


class PieAudioApp(MainWindow, ConfigAccessor):
    section = Sections.Shared

    signalPluginsReady = pyqtSignal()
    signalComponentsReady = pyqtSignal()
    signalComponentsLoading = pyqtSignal()

    def init(self) -> None:
        self.setWindowTitle("Pie Audio • Audio Converter ({})".format(
            Config.PIEAPP_VERSION
        ))
        self.setMinimumSize(720, 480)
        self.resize(*self.getConfig("ui.winsize", (720, 480), Sections.User))
        self.setWindowIcon(QIcon(self.getAsset("cloud.png")))

    def prepareSignals(self) -> None:
        self.signalPluginsReady.connect(self.notifyPluginReady)

    def prepare(self):
        self.prepareBaseSignals()
        self.prepareSignals()
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

    # Plugin method and signals

    def preparePlugins(self) -> None:
        """ Prepare all (or selected) Plugins """
        Managers(SysManagers.Menus).mount()
        Managers(SysManagers.Plugins).mount(self)
        self.signalPluginsReady.emit()

    def notifyPluginReady(self):
        self.getPlugin(Containers.StatusBar).showMessage(self.getTranslation("Plugins are ready"))

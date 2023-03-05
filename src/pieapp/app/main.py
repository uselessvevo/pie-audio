from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal

from pieapp.structs.containers import Containers
from piekit.system.loader import Config
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
        self.setLayout(self.mainHBox)

        self.mainHBox.setContentsMargins(0, 0, 0, 0)
        self.mainHBox.setSpacing(20)

        pixmap = QPixmap()
        pixmap.load(self.getAsset("empty-box.png"))

        widget = QtWidgets.QLabel()
        widget.setPixmap(pixmap)

        widget.setLayout(self.mainHBox)
        self.setCentralWidget(widget)

    # Plugin method and signals

    def preparePlugins(self) -> None:
        """ Prepare all (or selected) Plugins """
        Managers(SysManagers.Plugins).mount(self)
        self.signalPluginsReady.emit()

    def notifyPluginReady(self):
        self.getPlugin(Containers.StatusBar).showMessage(self.getTranslation("Plugins are ready"))

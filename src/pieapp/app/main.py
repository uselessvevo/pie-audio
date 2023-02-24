from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers, Sections
from piekit.mainwindow.main import MainWindow
from piekit.system.loader import Config


class PieAudioApp(MainWindow):
    section = Sections.Shared

    signalObjectsReady = pyqtSignal()
    signalComponentsReady = pyqtSignal()
    signalComponentsLoading = pyqtSignal()

    def init(self) -> None:
        self.setWindowTitle("Pie Audio • Audio Converter ({})".format(
            Config.PIEAPP_VERSION
        ))
        self.setMinimumSize(720, 480)
        self.resize(*Managers(SysManagers.Configs)(Sections.User, "ui.winsize", (720, 480)))
        self.setWindowIcon(QIcon(self.getAsset("cloud.png")))

    def prepareSignals(self) -> None:
        self.signalObjectsReady.connect(self.notifyObjectReady)

    def prepare(self):
        self.prepareBaseSignals()
        self.prepareSignals()
        self.prepareMainLayout()
        self.preparePieObjects()

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

    def preparePieObjects(self) -> None:
        """ Prepare all (or selected) PieObjects """
        Managers(SysManagers.Menus).mount()
        Managers(SysManagers.Objects).mount(self)
        self.signalObjectsReady.emit()

    def notifyObjectReady(self):
        self.getObject("status-bar").showMessage(self.getTranslation("Objects are ready"))

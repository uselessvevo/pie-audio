from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers, SharedSection
from piekit.mainwindow.main import MainWindow


class PieAudioApp(MainWindow):
    version = (0, 1, 0)
    section = SharedSection

    signalObjectsReady = pyqtSignal()
    signalComponentsReady = pyqtSignal()
    signalComponentsLoading = pyqtSignal()

    def init(self) -> None:
        self.setWindowTitle("Pie Audio • Audio Converter ({})".format(
            ".".join(str(i) for i in self.version)
        ))
        self.setMinimumSize(720, 480)
        self.resize(*self.getConfig("ui.winsize", (720, 480)))
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
        Managers.get(SysManagers.Objects).mount(self)
        self.signalObjectsReady.emit()

    def notifyObjectReady(self):
        self.getObject("status-bar").showMessage(self.getTranslation("Objects are ready"))

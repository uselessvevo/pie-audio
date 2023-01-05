import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from cloudykit.system.manager import System
from cloudykit.objects.structs import Error
from cloudykit.objects.plugin import BasePlugin
from cloudykit.objects.logger import logger


class MainWindow(QMainWindow):
    signalMoved = pyqtSignal()
    signalResized = pyqtSignal()
    signalExceptionOccurred = pyqtSignal(dict)

    signalPluginReady = pyqtSignal(str)
    signalPluginLoading = pyqtSignal(str)
    signalPluginReloading = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Set windows taskbar icon
        if os.name == "nt":
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "mycompany.myproduct.subproduct.version"
            )

        self._logger = logger
        self.__actions: dict = {}

    # Main methods

    def prepareBaseSignals(self) -> None:
        self.signalPluginReady.connect(self.pluginReady)
        self.signalPluginLoading.connect(self.pluginLoading)
        self.signalPluginReloading.connect(self.pluginReloading)
        self.signalExceptionOccurred.connect(self.errorHandler)

    # `ComponentsManager` interface methods

    def placeOn(self, child, target: str, **options) -> None:
        if not System.registry.components.get(target):
            raise ValueError(f"MainWindow doesn't contain component named `{target}`")

        if not isinstance(child, (BasePlugin,)):
            raise TypeError("MainWindow objects can register only `BasePlugin` based objects")

        # Register or render object on `BaseComponent` based object
        System.registry.components.get(target).register(child, **options)

    def removeFrom(self, child, target: str) -> None:
        if not isinstance(child, (BasePlugin,)):
            raise TypeError("MainWindow objects can register only `BasePlugin` based objects")

        if not System.registry.components.get(target):
            raise ValueError(f"MainWindow doesn't contain {target} object")

    # Event methods

    def closeEvent(self, event) -> None:
        System.registry.unmount()
        for window in QApplication.topLevelWindows():
            window.close()

    # Signals

    @pyqtSlot(str)
    def pluginLoading(self, name: str) -> None:
        pass

    @pyqtSlot(str)
    def pluginReady(self, name: str) -> None:
        pass

    @pyqtSlot(str)
    def pluginReloading(self, name: str) -> None:
        pass

    @pyqtSlot(Error)
    def errorHandler(self, error: Error) -> None:
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Critical)
        messageBox.setText(error.title)
        messageBox.setInformativeText(error.description)
        messageBox.setWindowTitle("Error")
        messageBox.exec_()

    # Properties

    @property
    def logger(self) -> logger:
        return self._logger

    @property
    def registry(self):
        return System.registry

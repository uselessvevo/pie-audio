import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from cloudykit.utils.logger import logger
from cloudykit.system import System
from cloudykit.plugins.base import BasePlugin
from cloudykit.system import SharedSection
from cloudykit.system import Error

from cloudykit.managers.assets.mixins import AssetsAccessor
from cloudykit.managers.configs.mixins import ConfigAccessor
from cloudykit.managers.locales.mixins import LocalesAccessor


class MainWindow(
    ConfigAccessor,
    AssetsAccessor,
    LocalesAccessor,
    QMainWindow,
):
    signalMoved = pyqtSignal()
    signalResized = pyqtSignal()
    signalExceptionOccurred = pyqtSignal(dict)

    signalPluginReady = pyqtSignal(str)
    signalPluginLoading = pyqtSignal(str)
    signalPluginReloading = pyqtSignal(str)

    def __init__(self, parent=None):
        ConfigAccessor.__init__(self, SharedSection)
        LocalesAccessor.__init__(self, SharedSection)
        AssetsAccessor.__init__(self, SharedSection)
        QMainWindow.__init__(self, parent=parent)

        # Just a logger
        self._logger = logger

        # Set windows taskbar icon
        if os.name == "nt":
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "mycompany.myproduct.subproduct.version"
            )

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
        # TODO: Add `ComponentsAccessor` and reimplement `mount/unmount` method
        System.registry.components.get(target).register(child, **options)

    def removeFrom(self, child, target: str) -> None:
        if not isinstance(child, (BasePlugin,)):
            raise TypeError("MainWindow objects can register only `BasePlugin` based objects")

        if not System.registry.components.get(target):
            raise ValueError(f"MainWindow doesn't contain {target} object")

    # Event methods

    def closeEvent(self, event) -> None:
        System.registry.unmount(full_house=True)
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
        messageBox.setWindowTitle(self.getTranslation("Error"))
        messageBox.exec_()

    # Properties

    @property
    def logger(self) -> logger:
        return self._logger

    @property
    def registry(self):
        return System.registry

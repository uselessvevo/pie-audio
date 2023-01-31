import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from cloudykit.managers.assets.mixins import AssetsMixin
from cloudykit.managers.configs.mixins import ConfigMixin
from cloudykit.managers.locales.mixins import LocalesMixin
from cloudykit.system.types import Error
from cloudykit.system.manager import System
from cloudykit.utils.logger import logger
from cloudykit.plugins.base import BasePlugin


class AppWindow(QMainWindow, ConfigMixin, LocalesMixin, AssetsMixin):
    signalMoved = pyqtSignal()
    signalResized = pyqtSignal()
    signalExceptionOccurred = pyqtSignal(dict)

    signalPluginReady = pyqtSignal(str)
    signalPluginLoading = pyqtSignal(str)
    signalPluginReloading = pyqtSignal(str)

    def __init__(self):
        super().__init__(section="shared")

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
            raise ValueError(f"AppWindow doesn't contain component named `{target}`")

        if not isinstance(child, (BasePlugin,)):
            raise TypeError("AppWindow objects can register only `BasePlugin` based objects")

        # Register or render object on `BaseComponent` based object
        System.registry.components.get(target).register(child, **options)

    def removeFrom(self, child, target: str) -> None:
        if not isinstance(child, (BasePlugin,)):
            raise TypeError("AppWindow objects can register only `BasePlugin` based objects")

        if not System.registry.components.get(target):
            raise ValueError(f"AppWindow doesn't contain {target} object")

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
        messageBox.setWindowTitle("Error")
        messageBox.exec_()

    # Properties

    @property
    def logger(self) -> logger:
        return self._logger

    @property
    def registry(self):
        return System.registry

import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from piekit.managers.plugins.mixins import PluginsAccessor
from piekit.utils.logger import logger
from piekit.plugins.base import BasePlugin
from piekit.managers.registry import Managers

from piekit.structs.etc import Error
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class MainWindow(
    QMainWindow,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    PluginsAccessor
):
    # Accessors section
    section: str = "shared"

    signalMoved = pyqtSignal()
    signalResized = pyqtSignal()
    signalExceptionOccurred = pyqtSignal(dict)

    signalPluginReady = pyqtSignal(str)
    signalPluginLoading = pyqtSignal(str)
    signalPluginReloading = pyqtSignal(str)

    def __init__(self, parent=None):
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
        if not Managers.components.get(target):
            raise ValueError(f"MainWindow doesn't contain component named `{target}`")

        if not isinstance(child, (BasePlugin,)):
            raise TypeError("MainWindow objects can register only `BasePlugin` based objects")

        # Register or render object on `BaseComponent` based object
        # TODO: Add `ComponentsAccessor` and reimplement `mount/unmount` method
        Managers.plugins.get(target).register(child, **options)

    def removeFrom(self, child, target: str) -> None:
        if not isinstance(child, (BasePlugin,)):
            raise TypeError("MainWindow objects can register only `BasePlugin` based objects")

        if not Managers.plugins.get(target):
            raise ValueError(f"MainWindow doesn't contain {target} object")

    # Event methods

    def closeEvent(self, event) -> None:
        Managers.unmount(full_house=True)
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
        return Managers

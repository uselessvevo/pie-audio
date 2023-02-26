from pathlib import Path
from typing import Union

from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

from piekit.utils.logger import logger
from piekit.widgets.messagebox import MessageBox

from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers

from piekit.plugins.types import PluginTypes, Error
from piekit.plugins.observer import PluginsObserverMixin


class PiePlugin(
    QObject,
    PluginsObserverMixin,
):
    type = PluginTypes.Plugin

    # Icon name
    icon: Union[None, str] = "app.png"

    # By default, description must be written in English
    description: str = None

    # Main attributes #

    # Plugin codename
    name: str

    type: str = PluginTypes.Plugin

    # Accessors section
    section: str = None

    # PiePlugin version
    version: tuple[int] = (0, 1, 0)

    # List of required built-in plugins
    requires: list[str] = []

    # List of optional built-in plugins
    optional: list[str] = []

    # Qt configuration #

    # Signal when plugin is ready
    signalPluginReady = pyqtSignal()

    # Signal when plugin is loading
    signalPluginLoading = pyqtSignal(str)

    # Signal when plugin is reloading
    signalPluginReloading = pyqtSignal(str)

    # Signal when main window is closing
    signalOnMainWindowClose = pyqtSignal()

    # Signal when exception occurred
    signalExceptionOccurred = pyqtSignal(Error)

    def __init__(
        self,
        parent: QObject = None,
        path: Path = None,
    ) -> None:
        super().__init__(parent)

        # Just a logger
        self._logger = logger

        # Parent object/window
        self._parent = parent

        # PiePlugin path
        self._path: Path = path

        self._managers: list["BaseManager"] = []

    # Main methods

    def prepare(self) -> None:
        # First, we need to initialize base signals
        self.prepareBaseSignals()

        # PiePlugin is loading
        self.signalPluginLoading.emit(self.__class__.__name__)

        # Initializing plugin
        self.init()

    # Signals, shortcuts etc. methods

    def prepareBaseSignals(self):
        self.logger.info(f"Preparing base signals for {self.__class__.__name__}")
        self.signalPluginLoading.connect(self._parent.signalPluginLoading)
        self.signalPluginReloading.connect(self._parent.signalPluginReloading)
        self.signalExceptionOccurred.connect(self.errorHandler)

    def prepareShortcuts(self) -> None:
        """ Prepare plugin shortcuts and register them in `ShortcutsManager` """
        pass

    def prepareConfigurationPage(self) -> None:
        """ Prepare configuration page widget """
        pass

    # Render methods

    def init(self) -> None:
        """ Initialize an object. For example, render it """
        raise NotImplementedError("Method `init` must be implemented")

    # Update methods

    def updateStyle(self) -> None:
        pass

    def updateLocalization(self) -> None:
        pass

    # Getter methods

    def getDescription(self) -> str:
        return self.description or f"{self.__class__.__class__}'s description"

    def getName(self) -> str:
        return self.name or self.__class__.__name__

    def getVersion(self) -> tuple[int]:
        return self.version

    # Event methods

    def close(self, event) -> None:
        if self.closeHandler(True):
            event.accept()
        else:
            event.ignore()

    def closeHandler(self, cancellable: bool = True) -> bool:
        if cancellable and Managers(SysManagers.Configs)("ui.show_exit_dialog", self.name, True):
            messageBox = MessageBox(self)
            if messageBox.clickedButton() == messageBox.noButton:
                return False

        QApplication.processEvents()
        Managers.unmount(full_house=True)

        return True

    # Slots

    @pyqtSlot(Error)
    def errorHandler(self, error: Error) -> None:
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Critical)
        messageBox.setText(error.title)
        messageBox.setInformativeText(error.description)
        messageBox.setWindowTitle(Managers(SysManagers.Locales)("Error", section="shared"))
        messageBox.exec_()

    # Properties

    @property
    def logger(self):
        return self._logger

    @property
    def path(self) -> Path:
        return self._path

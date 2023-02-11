from pathlib import Path
from typing import Union

from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from piekit.utils.logger import logger

from piekit.structs.etc import Error
from piekit.structs.etc import SharedSection

from piekit.plugins.mixins import MenuMixin
from piekit.plugins.mixins import ActionMixin
from piekit.plugins.observers import PluginObserverMixin

from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class BasePlugin(
    QObject,
    PluginObserverMixin,
    ActionMixin,
    MenuMixin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    # Main attributes #

    # BasePlugin codename
    name: str

    # Accessors section
    section: str = SharedSection

    # Icon name
    icon: str = "app.ico"

    # By default, description must be written in English
    description: str

    # BasePlugin version
    version: tuple[int] = (0, 1, 0)

    # List of required built-in plugins
    requires: list[str] = []

    # List of optional built-in plugins
    optional: list[str] = []

    container: Union[None, QWidget] = None

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

        # BasePlugin path
        self._path: Path = path

        self._managers: list["BaseMager"] = []

        # Flag: is plugin registered
        self._is_registered: bool = False

    # Main methods

    def prepare(self) -> None:
        # First, we need to initialize base signals
        self.prepareBaseSignals()

        # BasePlugin is loading
        self.signalPluginLoading.emit(self.__class__.__name__)

        # Initializing plugin
        self.init()

        # BasePlugin is ready
        self.signalPluginReady.emit()

        # Inform about that
        self.logger.info(f"Plugin {self.name} is ready!")

    # Signals, shortcuts etc. methods

    def prepareBaseSignals(self):
        self.logger.info(f"Preparing base signals for {self.__class__.__name__}")
        self.signalPluginLoading.connect(self._parent.signalPluginLoading)
        self.signalPluginReloading.connect(self._parent.signalPluginReloading)
        self.signalExceptionOccurred.connect(self.errorHandler)

    def prepareShortcuts(self) -> None:
        """ Prepare plugin's shortcuts and register them in `ShortcutsManager` """
        pass

    def prepareConfigurationPage(self) -> None:
        """ Prepare configuration page widget """
        pass

    # Render methods

    def renderOnParent(self) -> None:
        """ Render plugin on parent's component """
        pass

    def init(self, *args, **kwargs) -> None:
        """ Call/render plugin with given arguments """
        raise NotImplementedError("Method `call` must be implemented")

    # Update methods

    def updateStyle(self) -> None:
        pass

    def updateLocalization(self) -> None:
        pass

    def onCloseEvent(self) -> None:
        self.logger.info("Closing. Goodbye!..")

    # Getter methods

    def getTitle(self) -> str:
        version = ".".join(str(i) for i in self.version)
        return f"{self.name} • {version}"

    def getName(self) -> str:
        return self.name or self.__class__.__name__

    def getDescription(self) -> str:
        return self.description or f"{self.__class__.__class__}'s description"

    def getVersion(self) -> tuple[int]:
        return self.version

    def getIcon(self) -> str:
        return self.getAsset("app.ico") \
               or self.getAsset("debug.svg", section=SharedSection)

    # Signals

    @pyqtSlot(Error)
    def errorHandler(self, error: Error) -> None:
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Critical)
        messageBox.setText(error.title)
        messageBox.setInformativeText(error.description)
        messageBox.setWindowTitle(self.getTranslation("Error", section="shared"))
        messageBox.exec_()

    # Properties

    @property
    def logger(self):
        return self._logger

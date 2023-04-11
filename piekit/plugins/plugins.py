from pathlib import Path
from typing import Union

from PySide6.QtCore import Signal, QObject

from piekit.utils.logger import logger
from piekit.managers.base import BaseManager
from piekit.plugins.types import PluginTypes, Error
from piekit.plugins.observer import PluginsObserverMixin


class PiePlugin(
    QObject,
    PluginsObserverMixin,
):
    # Main attributes #

    # Plugin type
    type: PluginTypes = PluginTypes.Plugin

    # Icon name
    icon: Union[None, str] = "app.png"

    # By default, description must be written in English
    description: str = None

    # Plugin codename
    name: str

    # Accessors section
    section: str = None

    # PiePlugin version
    version: tuple[int] = (0, 1, 0)

    # List of required built-in plugins
    requires: list[str] = []

    # List of optional built-in plugins
    optional: list[str] = []

    api: "PiePluginAPI" = None

    # Qt configuration #

    # Signal when plugin is ready
    signalPluginReady = Signal()

    # Signal when plugin is loading
    signalPluginLoading = Signal(str)

    # Signal when plugin is reloading
    signalPluginReloading = Signal(str)

    # Signal when main window is closing
    signalOnMainWindowClose = Signal()

    # Signal when exception occurred
    signalExceptionOccurred = Signal(Error)

    def __init__(
        self,
        parent: QObject = None,
        path: Path = None,
    ) -> None:
        # For some reason, I can't use `super().__init__()` method with `PySide`

        # Initialize `QObject` instance
        QObject.__init__(self, parent)

        # Initialize `PluginsObserverMixin` instance
        PluginsObserverMixin.__init__(self)

        # Just a logger
        self._logger = logger

        # Parent object/window
        self._parent = parent

        # PiePlugin path
        self._path: Path = path

        self._managers: list[BaseManager] = []

    # Main methods

    def prepare(self) -> None:
        # First, we need to initialize base signals
        self.prepareBaseSignals()

        # PiePlugin is loading
        self.signalPluginLoading.emit(self.__class__.__name__)

        # Initializing plugin
        self.init()

        # Prepare PiePluginAPI
        self.prepareAPI()

    # Signals, shortcuts etc. methods

    def prepareAPI(self) -> None:
        """
        Method that prepare PiePluginAPI based instance
        """
        from piekit.plugins.api.api import PiePluginAPI

        if self.api and issubclass(self.api, PiePluginAPI):
            self.api = self.api(self)
            self.api.init()

    def prepareBaseSignals(self):
        self.logger.info(f"Preparing base signals for {self.__class__.__name__}")
        self.signalPluginLoading.connect(self._parent.signalPluginLoading)
        self.signalPluginReloading.connect(self._parent.signalPluginReloading)
        self.signalExceptionOccurred.connect(self._parent.errorHandler)

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

    # Properties

    @property
    def logger(self):
        return self._logger

    @property
    def path(self) -> Path:
        return self._path

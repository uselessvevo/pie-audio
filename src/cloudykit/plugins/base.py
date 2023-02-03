from pathlib import Path

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from cloudykit.system.types import Error
from cloudykit.system.manager import System
from cloudykit.system.registry import ManagersRegistry

from cloudykit.utils.logger import logger
from cloudykit.system.types import PathConfig
from cloudykit.plugins.mixins import MenuMixin
from cloudykit.plugins.mixins import ActionMixin
from cloudykit.components.mixins import ComponentMixin


class BasePlugin(
    QWidget,
    ActionMixin,
    MenuMixin,
    ComponentMixin
):
    # Main attributes #

    # Plugin codename
    name: str

    # Icon name
    icon: str = "app.ico"

    # By default, description must be written in English
    description: str

    # Plugin version
    version: tuple[int] = (0, 1, 0)

    # Required builtin plugins
    plugins: list[str]
    
    # Required components
    components: list[str]

    # Qt configuration #

    # Mininal window size
    minSize: tuple[int, int] = (355, 205)

    # Maximum window size
    maxSize: tuple[int, int] = (720, 450)

    # Signal when plugin is ready
    signalPluginReady = pyqtSignal(str)
    
    # Signal when plugin is loading
    signalPluginLoading = pyqtSignal(str)
    
    # Signal when plugin is reloading
    signalPluginReloading = pyqtSignal(str)

    # Signal when main window is closing
    signalOnMainWindowClose = pyqtSignal()
    
    # Signal when exception occurred
    signalExceptionOccurred = pyqtSignal(Error)

    def __init__(self, parent: QObject = None, path: Path = None):
        super().__init__()

        # Just a logger
        self._logger = logger

        # Parent object/window
        self._parent = parent

        # Plugin path
        self._path: Path = path

        # Flag: is plugin registered
        self._is_registered: bool = False

    # Main methods

    def mount(self) -> None:
        """ Mount managers """
        System.registry.configs.mount(PathConfig(self._path, section=self.name))
        System.registry.locales.mount(PathConfig(self._path, section=self.name))
        System.registry.assets.mount(PathConfig(self._path, section=self.name))

    def unmount(self) -> None:
        System.registry.configs.delete(self.name)
        System.registry.locales.delete(self.name)
        System.registry.assets.delete(self.name)

    def init(self) -> None:
        # First, we need to initialize base signals
        self.prepareBaseSignals()

        # Plugin is loading
        self.signalPluginLoading.emit(self.__class__.__name__)

        # Preparing managers
        self.mount()

        # Render on AppWindow's components
        self.renderOnWindow()

        # Plugin is ready
        self.signalPluginReady.emit(self.__class__.__name__)

        # Inform about that
        self.logger.info(f"Plugin {self.name} is ready!")

    # Signals, shortcuts etc. methods

    def prepareBaseSignals(self):
        self.logger.info(f"Preparing base signals for {self.__class__.__name__}")
        self.signalPluginReady.connect(self._parent.signalPluginReady)
        self.signalPluginLoading.connect(self._parent.signalPluginLoading)
        self.signalPluginReloading.connect(self._parent.signalPluginReloading)
        self.signalExceptionOccurred.connect(self.errorHandler)

    def prepareShortcuts(self) -> None:
        pass

    def prepareConfiguratinPage(self) -> None:
        pass

    # Render methods

    def renderOnWindow(self) -> None:
        """ Render plugin on AppWindow's components """
        pass

    def renderWindow(self) -> None:
        """ Render plugin's window """
        pass

    def prepareSizes(self) -> None:
        self.setMinimumSize(*self.minSize)
        self.setMaximumSize(*self.maxSize)

    def updateStyle(self) -> None:
        pass

    def refresh(self) -> None:
        pass

    # Event methods

    def onShow(self, *args, **kwargs) -> None:
        pass

    def show(self) -> None:
        self.onShow()
        super().show()

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
        return System.registry.assets.get(self.icon)

    # Signals

    @pyqtSlot(Error)
    def errorHandler(self, error: Error) -> None:
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Critical)
        messageBox.setText(error.title)
        messageBox.setInformativeText(error.description)
        messageBox.setWindowTitle(System.registry.locales("shared", "Error"))
        messageBox.exec_()

    # Properties

    @property
    def logger(self):
        return self._logger

    @property
    def registry(self) -> ManagersRegistry:
        return System.registry

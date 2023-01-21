from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from cloudykit.objects.structs import Error
from cloudykit.system.manager import System
from cloudykit.system.registry import ManagersRegistry

from cloudykit.objects.logger import logger
from cloudykit.objects.mixins import MenuMixin
from cloudykit.objects.mixins import ActionMixin
from cloudykit.objects.mixins import ComponentMixin


class BasePlugin(
    QWidget,
    ActionMixin,
    MenuMixin,
    ComponentMixin
):
    # Base configuration #

    # Plugin codename
    name: str

    # Icon name
    icon: str = "app.ico"

    # By default, description must be written in English
    description: str

    # Plugin version
    version: tuple[int, int, int] = (0, 1, 0)

    # Required plugins
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

    def __init__(self, parent: QObject = None):
        super().__init__()

        self._parent = parent
        self._is_registered: bool = False
        self._logger = logger
        self._path: "Path" = System.root / System.config.PLUGINS_FOLDER_NAME / self.name

    def prepareBaseSignals(self):
        self.logger.info(f"Preparing base signals for {self.__class__.__name__}")
        self.signalPluginReady.connect(self._parent.signalPluginReady)
        self.signalPluginLoading.connect(self._parent.signalPluginLoading)
        self.signalPluginReloading.connect(self._parent.signalPluginReloading)
        self.signalExceptionOccurred.connect(self.errorHandler)

    # Main methods

    def init(self) -> None:
        # First, we need to init all base signals
        self.prepareBaseSignals()

        # Emit that our plugin is loading
        self.signalPluginLoading.emit(self.__class__.__name__)

        # Call `mount` method
        self.mount()

        # Emit that we're ready
        self.signalPluginReady.emit(self.__class__.__name__)

        # Inform about that
        self.logger.info(f"Plugin {self.name} is ready!")

    def mount(self) -> None:
        """
        Mount plugin.
        For example, you can use `placeOn` method to render it on `MainWindow` components
        """
        raise NotImplementedError("Method `mount` must be implemented")

    def unmount(self) -> None:
        self.logger.info("Unmounting. Goodbye!..")

    # Event methods

    def onShow(self, *args, **kwargs) -> None:
        pass

    def show(self) -> None:
        self.onShow()
        super().show()

    def onCloseEvent(self) -> None:
        self.logger.info("Closing. Goodbye!..")

    # Render methods

    def prepareSizes(self) -> None:
        self.setMinimumSize(*self.minSize)
        self.setMaximumSize(*self.maxSize)

    def updateStyle(self) -> None:
        pass

    def refresh(self) -> None:
        pass

    # Getter methods

    def getTitle(self) -> str:
        version = ".".join(str(i) for i in self.version)
        return f"{self.name} • {version}"

    def getName(self) -> str:
        return self.name or self.__class__.__name__

    def getDescription(self) -> str:
        return self.description or f"{self.__class__.__class__}'s description"

    def getVersion(self) -> tuple[int, int, int]:
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
        messageBox.setWindowTitle("Error")
        messageBox.exec_()

    # Properties

    @property
    def logger(self):
        return self._logger

    @property
    def registry(self) -> ManagersRegistry:
        return System.registry

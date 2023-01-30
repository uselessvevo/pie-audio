from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from cloudykit.system.types import Error
from cloudykit.utils.logger import logger
from cloudykit.system.manager import System
from cloudykit.system.registry import ManagersRegistry


class BaseComponent(QObject):
    # Main attributes #

    # Component codename
    name: str

    # Component description
    description: str = f"{name} description"
    
    # Array of managers
    dependencies: tuple[str]

    # Qt configuration #

    # Signal when plugin is ready
    signalComponentReady = pyqtSignal(str)
    
    # Signal when plugin is loading
    signalComponentLoading = pyqtSignal(str)
    
    # Signal when plugin is reloading
    signalComponentReloading = pyqtSignal(str)

    # Signal when main window is closing
    signalOnMainWindowClose = pyqtSignal()
    
    # Signal when exception occurred
    signalExceptionOccurred = pyqtSignal(Error)

    def __init__(self, parent : QObject = None, *args, **kwargs) -> None:
        self._parent = parent
        self._is_registered: bool = False
        self._logger = logger
        self._path: "Path" = System.root / System.config.COMPONENTS_FOLDER / self.name

    def prepareBaseSignals(self):
        self.logger.info(f"Preparing base signals for {self.__class__.__name__}")
        self.signalComponentReady.connect(self._parent.signalComponentReady)
        self.signalComponentLoading.connect(self._parent.signalComponentLoading)
        self.signalComponentReloading.connect(self._parent.signalComponentReloading)
        self.signalExceptionOccurred.connect(self.errorHandler)

    def init(self) -> None:
        # First, we need to init all base signals
        self.prepareBaseSignals()

        # Emit that our plugin is loading
        self.signalComponentLoading.emit(self.__class__.__name__)

        # Call `mount` method
        self.mount()

        # Emit that we're ready
        self.signalComponentReady.emit(self.__class__.__name__)

        # Inform about that
        self.logger.info(f"Component {self.name} is ready!")

    def mount(self) -> None:
        raise NotImplementedError("Method `mount` must be implemented")

    def unmount(self) -> None:
        self._logger.info("Unmouting. Goodbye!..")

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
        messageBox.setWindowTitle("Component error")
        messageBox.exec_()

    # Properties

    @property
    def logger(self):
        return self._logger

    @property
    def registry(self) -> "ManagersRegistry":
        return System.registry

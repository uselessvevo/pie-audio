from pathlib import Path

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from cloudykit.system import Error, SharedSection
from cloudykit.system import System
from cloudykit.utils.logger import logger
from cloudykit.system.registry import ManagersRegistry

from cloudykit.managers.assets.mixins import AssetsAccessor
from cloudykit.managers.configs.mixins import ConfigAccessor
from cloudykit.managers.locales.mixins import LocalesAccessor


class BaseComponent(
    ConfigAccessor,
    AssetsAccessor,
    LocalesAccessor,
    QObject
):
    # Main attributes #

    # Component codename
    name: str

    version: tuple[int] = (0, 1, 0)

    # List of managers
    dependencies: tuple[str]

    sections: tuple[str]

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

    def __init__(self, parent: QObject = None, path: Path = None):
        ConfigAccessor.__init__(self, SharedSection)
        AssetsAccessor.__init__(self, SharedSection)
        LocalesAccessor.__init__(self, SharedSection)
        QObject.__init__(self, parent)

        # Just a logger
        self._logger = logger

        # Parent object/window
        self._parent = parent

        # Plugin path
        self._path: Path = path

        # Flag: is plugin registered
        self._is_registered: bool = False

    def mount(self) -> None:
        pass

    def unmount(self) -> None:
        pass

    def init(self) -> None:
        # First, we need to init all base signals
        self.prepareBaseSignals()

        # Emit that our plugin is loading
        self.signalComponentLoading.emit(self.__class__.__name__)

        # Prepare managers
        self.mount()

        # Render on parent's components
        self.renderOnParent()

        # Emit that we're ready
        self.signalComponentReady.emit(self.__class__.__name__)

        # Inform about that
        self.logger.info(f"Component {self.name} is ready!")

    def prepareBaseSignals(self):
        self.logger.info(f"Preparing base signals for {self.__class__.__name__}")
        self.signalComponentReady.connect(self._parent.signalComponentReady)
        self.signalComponentLoading.connect(self._parent.signalComponentLoading)
        self.signalComponentReloading.connect(self._parent.signalComponentReloading)
        self.signalExceptionOccurred.connect(self.errorHandler)

    def call(self, *args, **kwargs) -> None:
        """ Call component with given arguments """
        raise NotImplementedError("Method `call` must be implemented")

    def prepareShortcuts(self) -> None:
        pass

    def renderOnParent(self) -> None:
        """ Render plugin on parent's components """
        pass

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

    def getName(self) -> str:
        return self.name or self.__class__.__name__

    def getVersion(self) -> tuple[int]:
        return self.version

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

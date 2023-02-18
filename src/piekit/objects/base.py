from pathlib import Path

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from piekit.objects.types import ObjectTypes
from piekit.utils.logger import logger
from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers

from piekit.structs.etc import Error
from piekit.structs.etc import SharedSection
from piekit.objects.observer import PieObjectObserverMixin


class PieObject(
    QObject,
    PieObjectObserverMixin,
):
    # Main attributes #

    # PieObject codename
    name: str

    type: str = ObjectTypes.Pie

    # Accessors section
    section: str = SharedSection

    # BasePlugin version
    version: tuple[int] = (0, 1, 0)

    # List of required built-in pie_objects
    requires: list[str] = []

    # List of optional built-in pie_objects
    optional: list[str] = []

    # Qt configuration #

    # Signal when pie_object is ready
    signalObjectReady = pyqtSignal()

    # Signal when pie_object is loading
    signalObjectLoading = pyqtSignal(str)

    # Signal when pie_object is reloading
    signalObjectReloading = pyqtSignal(str)

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

        self._managers: list["BaseManager"] = []

    # Main methods

    def prepare(self) -> None:
        # First, we need to initialize base signals
        self.prepareBaseSignals()

        # BasePlugin is loading
        self.signalObjectLoading.emit(self.__class__.__name__)

        # Initializing pie_object
        self.init()

        # # BasePlugin is ready
        # self.signalObjectReady.emit()
        #
        # # Inform about that
        # self.logger.info(f"Object {self.name} is ready!")

    # Signals, shortcuts etc. methods

    def prepareBaseSignals(self):
        self.logger.info(f"Preparing base signals for {self.__class__.__name__}")
        self.signalObjectLoading.connect(self._parent.signalObjectLoading)
        self.signalObjectReloading.connect(self._parent.signalObjectReloading)
        self.signalExceptionOccurred.connect(self.errorHandler)

    def prepareShortcuts(self) -> None:
        """ Prepare object's shortcuts and register them in `ShortcutsManager` """
        pass

    def prepareConfigurationPage(self) -> None:
        """ Prepare configuration page widget """
        pass

    # Render methods

    def init(self) -> None:
        """ Initialize an object. For example, render it """
        raise NotImplementedError("Method `call` must be implemented")

    # Update methods

    def updateStyle(self) -> None:
        pass

    def updateLocalization(self) -> None:
        pass

    # Getter methods

    def getName(self) -> str:
        return self.name or self.__class__.__name__

    def getVersion(self) -> tuple[int]:
        return self.version

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

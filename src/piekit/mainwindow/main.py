import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from piekit.managers.objects.mixins import PluginsAccessor
from piekit.system.exceptions import PieException
from piekit.utils.logger import logger
from piekit.plugins.base import PiePlugin
from piekit.managers.registry import Managers

from piekit.objects.types import Error
from piekit.widgets.messagebox import MessageBox
from piekit.managers.types import Sections, SysManagers
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
    section: str = Sections.Shared

    signalMoved = pyqtSignal()
    signalResized = pyqtSignal()
    signalExceptionOccurred = pyqtSignal(dict)

    signalObjectReady = pyqtSignal(str)
    signalObjectLoading = pyqtSignal(str)
    signalObjectReloading = pyqtSignal(str)

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
        self.signalExceptionOccurred.connect(self.errorHandler)

    # Component interfaces

    def placeOn(self, child, target: str, **options) -> None:
        if not Managers.components.get(target):
            raise PieException(f"MainWindow doesn't contain component named `{target}`")

        if not isinstance(child, (PiePlugin,)):
            raise PieException("MainWindow objects can register only `PiePlugin` based objects")

        # Register or render object on `BaseComponent` based object
        # TODO: Add `ComponentsAccessor` and reimplement `mount/unmount` method
        Managers.objects.get(target).register(child, **options)

    def removeFrom(self, child, target: str) -> None:
        if not isinstance(child, (PiePlugin,)):
            raise PieException("MainWindow objects can register only `PiePlugin` based objects")

        if not Managers.objects.get(target):
            raise PieException(f"MainWindow doesn't contain {target} object")

    # Event methods

    def closeEvent(self, event) -> None:
        if self.closeHandler(True):
            event.accept()
        else:
            event.ignore()

    def closeHandler(self, cancellable: bool = True) -> bool:
        if cancellable and Managers(SysManagers.Configs)("ui.show_exit_dialog", Sections.User, True):
            messageBox = MessageBox(self)
            if messageBox.clickedButton() == messageBox.noButton:
                return False

        QApplication.processEvents()
        Managers.unmount(full_house=True)

        return True

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

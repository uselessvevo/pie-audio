import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from piekit.utils.logger import logger
from piekit.plugins.types import Error
from piekit.widgets.messagebox import MessageBox

from piekit.managers.structs import Sections
from piekit.managers.registry import Managers
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class MainWindow(
    QMainWindow,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    # Accessors section
    section: str = Sections.Shared

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
        self.signalExceptionOccurred.connect(self.errorHandler)

    # Event methods

    def closeEvent(self, event) -> None:
        if self.closeHandler(True):
            event.accept()
        else:
            event.ignore()

    def closeHandler(self, cancellable: bool = True) -> bool:
        if cancellable and self.getConfig("ui.show_exit_dialog", True, Sections.User):
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

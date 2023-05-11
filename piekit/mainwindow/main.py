import os

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox

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

    sig_moved = Signal()
    sig_resized = Signal()
    sig_exception_occurred = Signal(dict)

    sig_plugin_ready = Signal(str)
    sig_plugin_loading = Signal(str)
    sig_plugin_reloading = Signal(str)

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)

        # Just a logger
        self._logger = logger

        # Set windows taskbar icon
        if os.name == "nt":
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "com.crabdevs.pieaudio"
            )

    # Main methods

    def prepare_base_signals(self) -> None:
        self.sig_exception_occurred.connect(self.errorHandler)

    # Event methods

    def closeEvent(self, event) -> None:
        if self.closeHandler(True):
            event.accept()
        else:
            event.ignore()

    def closeHandler(self, cancellable: bool = True) -> bool:
        if cancellable and self.getConfig("ui.show_exit_dialog", True, Sections.User):
            messageBox = MessageBox(self)
            if messageBox.clickedButton() == messageBox.no_button:
                return False

        QApplication.processEvents()
        Managers.shutdown(full_house=True)

        return True

    @Slot(Error)
    def errorHandler(self, error: Error) -> None:
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Critical)
        messageBox.setText(error.title)
        messageBox.setInformativeText(error.description)
        messageBox.setWindowTitle(self.getTranslation("Error"))
        messageBox.exec()

    # Properties

    @property
    def logger(self) -> logger:
        return self._logger

    @property
    def registry(self):
        return Managers

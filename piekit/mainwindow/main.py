from __feature__ import snake_case

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
        self.sig_exception_occurred.connect(self.error_handler)

    # Event methods

    def close_event(self, event) -> None:
        if self.close_handler(True):
            event.accept()
        else:
            event.ignore()

    def close_handler(self, cancellable: bool = True) -> bool:
        if cancellable and self.get_config("ui.show_exit_dialog", True, Sections.User):
            message_box = MessageBox(self)
            if message_box.clicked_button() == message_box.no_button:
                return False

        QApplication.process_events()
        Managers.shutdown(full_house=True)

        return True

    @Slot(Error)
    def error_handler(self, error: Error) -> None:
        message_box = QMessageBox()
        message_box.set_icon(QMessageBox.Icon.Critical)
        message_box.set_text(error.title)
        message_box.set_informative_text(error.description)
        message_box.set_window_title(self.get_translation("Error"))
        message_box.exec()

    # Properties

    @property
    def logger(self) -> logger:
        return self._logger

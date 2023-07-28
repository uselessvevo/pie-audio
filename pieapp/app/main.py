from __feature__ import snake_case

from PySide6.QtGui import Qt

import os

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QMainWindow

from piekit.config import Config
from piekit.utils.logger import logger
from piekit.managers.structs import Section
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.plugins.mixins import ErrorWindowMixin, QuitMixin


class PieAudioApp(
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    QuitMixin,
    ErrorWindowMixin,
    QMainWindow,
):
    # Accessors section
    section: str = Section.Shared
    name = Config.PIEAPP_APPLICATION_NAME

    # Base signals
    sig_moved = Signal()
    sig_resized = Signal()
    sig_exception_occurred = Signal(dict)

    sig_plugins_ready = Signal()
    sig_plugin_ready = Signal(str)
    sig_plugin_loading = Signal(str)
    sig_plugin_reloading = Signal(str)
    sig_restart_requested = Signal(str)

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)

        # Just a logger
        self._logger = logger

        # Set windows taskbar icon
        if os.name == "nt":
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                Config.PIEAPP_ORGANIZATION_DOMAIN
            )

    def init(self) -> None:
        self.prepare_base_signals()
        self.prepare_main_window()
        self.prepare_main_layout()
        self.prepare_workbench_layout()
        self.prepare_table_layout()
        self.prepare_central_widget()

    def prepare_base_signals(self) -> None:
        self.sig_restart_requested.connect(self.close_event)
        self.sig_exception_occurred.connect(self.error_handler)

    def prepare_main_window(self) -> None:
        self.set_minimum_size(*Config.MAIN_WINDOW_MIN_WINDOW_SIZE)
        self.resize(*self.get_config("ui.winsize", Config.MAIN_WINDOW_MIN_WINDOW_SIZE, Section.User))
        self.set_window_title(f'{self.get_translation("Pie Audio • Audio Converter")} '
                              f'({Config.PIEAPP_APPLICATION_VERSION})')
        self.set_window_icon(self.get_asset_icon("cloud.png"))

    def prepare_main_layout(self) -> None:
        self.main_layout = QGridLayout()
        self.main_layout.set_spacing(0)
        self.main_layout.set_contents_margins(0, 0, 0, 0)
        self.main_layout.set_alignment(Qt.AlignmentFlag.AlignHCenter)
        self.set_layout(self.main_layout)

    def prepare_workbench_layout(self) -> None:
        self.workbench_layout = QGridLayout()
        self.main_layout.add_layout(self.workbench_layout, 0, 0, Qt.AlignmentFlag.AlignTop)

    def prepare_table_layout(self) -> None:
        self.table_layout = QGridLayout()
        self.main_layout.add_layout(self.table_layout, 1, 0, Qt.AlignmentFlag.AlignTop)

    def prepare_central_widget(self):
        widget = QtWidgets.QLabel()
        widget.set_layout(self.main_layout)
        self.set_central_widget(widget)

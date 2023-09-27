from __feature__ import snake_case

from PySide6.QtGui import Qt

import os

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow

from piekit.globals import Global
from piekit.layouts.layouts import MainGridLayout
from piekit.managers.layouts.mixins import LayoutsAccessorMixin
from piekit.managers.structs import Section
from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.plugins.mixins import ErrorDialogMixin, QuitDialogMixin


class MainWindow(
    LayoutsAccessorMixin, QuitDialogMixin, ErrorDialogMixin,
    ConfigAccessorMixin, LocalesAccessorMixin, AssetsAccessorMixin,
    QMainWindow,
):
    # Accessors section
    section: str = Section.Shared

    # Signals
    sig_moved = Signal()
    sig_resized = Signal()
    sig_exception_occurred = Signal(dict)

    # Plugin signals
    sig_plugins_ready = Signal()
    sig_plugin_ready = Signal()
    sig_plugin_loading = Signal()
    sig_plugin_reloading = Signal()
    sig_restart_requested = Signal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)

        # Set windows taskbar icon
        if os.name == "nt":
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                Global.PIEAPP_ORGANIZATION_DOMAIN
            )

    def init(self) -> None:
        self.prepare_base_signals()
        self.prepare_main_window()
        self.prepare_main_layout()
        self.prepare_central_widget()

    def prepare_base_signals(self) -> None:
        self.sig_restart_requested.connect(self.close_event)
        self.sig_exception_occurred.connect(self.error_handler)

    def prepare_main_window(self) -> None:
        self.set_minimum_size(*Global.MAIN_WINDOW_MIN_WINDOW_SIZE)
        self.resize(*self.get_config(
            key="ui.winsize",
            default=Global.MAIN_WINDOW_MIN_WINDOW_SIZE,
            scope=Section.Root,
            section=Section.User
        ))
        self.set_window_title(
            f'{self.get_translation("Pie Audio • Audio Converter")} '
            f'({Global.PIEAPP_APPLICATION_VERSION})'
        )
        self.set_window_icon(self.get_svg_icon("cloud.svg"))

    def prepare_main_layout(self) -> None:
        self.main_layout = MainGridLayout()
        self.main_layout.set_spacing(0)
        self.main_layout.set_contents_margins(0, 0, 0, 0)
        self.main_layout.set_alignment(Qt.AlignmentFlag.AlignHCenter)
        self.set_layout(self.main_layout)
        self.register_layout(self.main_layout)

    def prepare_central_widget(self):
        widget = QtWidgets.QLabel()
        widget.set_layout(self.main_layout)
        self.set_central_widget(widget)

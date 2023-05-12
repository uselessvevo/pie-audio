from __feature__ import snake_case

from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGridLayout

from piekit.config import Config
from pieapp.structs.containers import Containers
from piekit.plugins.utils import get_plugin
from piekit.mainwindow.main import MainWindow
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections
from piekit.managers.configs.mixins import ConfigAccessor


class PieAudioApp(MainWindow, ConfigAccessor):
    name = Config.PIEAPP_NAME
    section = Sections.Shared
    sig_plugins_ready = Signal()

    def init(self) -> None:
        self.set_window_title("Pie Audio • Audio Converter ({})".format(
            Config.PIEAPP_VERSION
        ))
        self.set_minimum_size(720, 480)
        self.resize(*self.get_config("ui.winsize", Config.MAIN_WINDOW_DEFAULT_WINDOW_SIZE, Sections.User))
        self.set_window_icon(QIcon(self.get_asset("cloud.png")))

    def prepare_signals(self) -> None:
        self.sig_plugins_ready.connect(self.notify_plugins_ready)

    def prepare(self):
        self.prepare_base_signals()
        self.prepare_main_layout()
        self.prepare_workbench_layout()
        self.prepare_table_layout()
        self.prepare_central_widget()
        self.prepare_plugins()

    def prepare_main_layout(self) -> None:
        self.main_layout = QGridLayout()
        self.set_layout(self.main_layout)

    def prepare_workbench_layout(self) -> None:
        self.workbench_layout = QGridLayout()
        self.main_layout.add_layout(self.workbench_layout, 0, 0)

    def prepare_table_layout(self) -> None:
        self.table_layout = QGridLayout()
        self.main_layout.add_layout(self.table_layout, 1, 0)

    def prepare_central_widget(self):
        widget = QtWidgets.QLabel()
        widget.set_layout(self.main_layout)
        self.set_central_widget(widget)

    # Plugin method and signals

    def prepare_plugins(self) -> None:
        """ Prepare all (or selected) Plugins """
        Managers(SysManagers.Plugins).init(self)
        self.sig_plugins_ready.emit()

    def notify_plugins_ready(self):
        get_plugin(Containers.StatusBar).show_message(self.get_translation("Plugins are ready"))

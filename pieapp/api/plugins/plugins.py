from __future__ import annotations

from pathlib import Path
from typing import Any, Type

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from pieapp.api.converter.models import MediaFile
from pieapp.api.exceptions import PieError
from pieapp.api.plugins.types import PluginType
from pieapp.api.plugins.widgets import PiePluginWidget, PiePluginDockableWidget
from pieapp.api.plugins.observer import PluginsObserverMixin


class PieBasePlugin(QObject, PluginsObserverMixin):
    """
    PieBasePlugin is a base plugin class.
    """
    # Plugin/manager name
    name: str

    # Plugin type
    type: str = PluginType.Plugin

    # List of required built-in plugins
    requires: list[str] = []

    # List of optional built-in plugins
    optional: list[str] = []

    # Signals

    # Emit when all plugins are ready
    sig_reg_plugins_ready = Signal()

    # Emit when all plugins are about to teardown
    sig_reg_plugins_teardown = Signal()

    # Emit when plugin is about to teardown
    sig_plugin_teardown = Signal(str)

    # Signal when plugin is ready
    sig_plugin_ready = Signal()

    # Signal when plugin is loading
    sig_plugin_loading = Signal(str)

    # Signal when plugin is reloading
    sig_plugin_reloading = Signal(str)

    # Signal when exception occurred
    sig_exception_occurred = Signal(PieError)

    # Emit before main window shown
    sig_on_before_main_window_show = Signal()

    # Emit on main window shown
    sig_on_main_window_show = Signal()

    # Emit on main window close
    sig_on_main_window_close = Signal()

    def __init__(self, parent: QMainWindow = None, path: Path = None) -> None:
        # Initialize `QObject` instance
        QObject.__init__(self, parent)

        # Initialize `PluginsObserverMixin` instance
        PluginsObserverMixin.__init__(self)

        # Parent object/window
        self._parent = parent

        # PiePlugin path
        self._path: Path = path

        # Widget placeholder
        self._widget = None

    # Initialization methods

    def connect_signals(self) -> None:
        # Connect `PluginRegistry` event signals
        self.sig_reg_plugins_ready.connect(self.on_plugins_ready)
        self.sig_reg_plugins_teardown.connect(self.on_plugins_teardown)

        # Connect MainWindow signals
        self.sig_on_before_main_window_show.connect(self.on_before_main_window_show)
        self.sig_on_main_window_show.connect(self.on_main_window_show)
        self.sig_on_main_window_close.connect(self.on_main_window_close)

        # Connect main signals
        self.sig_plugin_teardown.connect(self.on_plugin_teardown)

    def prepare(self) -> None:
        """
        Prepares the plugin by calling `init` method and emitting `signals.plugin_ready` signal.
        """
        self.connect_signals()
        self.init()
        self.sig_plugin_ready.emit()

    def init(self) -> None:
        """
        Initializes the plugin and required services after forming an instance of the class
        """

    def call(self, *args, **kwargs) -> None:
        """
        This method calls the plugin.
        For example, it is usually used to display an already prepared plugin widget (window).
        In rare cases the whole thing is rendered anew.
        """
        raise NotImplementedError(f"Method \"call\" must be implemented")

    def get_plugin_icon(self) -> "QIcon":
        """
        This method returns the plugin icon
        """
        return QIcon()

    def get_widget(self) -> Any:
        if self._widget is None:
            raise PieError("Plugin must have an initialized `widget_class` field")

        return self._widget

    @staticmethod
    def get_name() -> str:
        """
        This method returns the translated name of the plugin
        """
        raise NotImplementedError(f"Method \"get_name\" must be implemented")

    def get_title(self) -> str:
        raise NotImplementedError(f"Method \"get_title\" must be implemented ({self.__class__.__name__})")

    @staticmethod
    def get_description() -> str:
        """
        This method returns the translated description of the plugin
        """
        return "No description provided"

    # Event methods

    def on_plugins_ready(self) -> None:
        pass

    def on_plugins_teardown(self) -> None:
        pass

    def on_plugin_teardown(self, name: str) -> None:
        pass

    def before_main_window_visible(self) -> None:
        pass

    def on_before_main_window_show(self) -> None:
        pass

    def on_main_window_show(self) -> None:
        pass

    def on_main_window_close(self) -> None:
        pass

    def on_close(self) -> None:
        pass

    def can_close(self) -> bool:
        return True

    def get_path(self) -> Path:
        """
        This method returns the full path of the plugin
        """
        return self._path

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <name: {self.name}, type: {self.type}>"


class PiePlugin(PieBasePlugin):

    # Plugin widget class
    widget_class: Type[PiePluginWidget] = None

    def prepare_widget(self) -> None:
        """
        Initialize plugin's widget
        """
        if self.widget_class:
            self._widget = self.widget_class(self._parent, self)
            if isinstance(self._widget, (PiePluginWidget, PiePluginDockableWidget, PieMediaPlugin)):
                self._widget.set_icon(self.get_plugin_icon())
                self._widget.set_title(self.get_title())
                self._widget.prepare()
                self._widget.init()
            else:
                raise PieError("The `widget` field of plugin must be a subclass of PiePluginWidget")

    def prepare(self) -> None:
        """
        Prepares the plugin by calling `init` method and emitting `signals.plugin_ready` signal.
        """
        self.connect_signals()
        self.prepare_widget()
        self.init()
        self.sig_plugin_ready.emit()


class PieDockablePlugin(PiePlugin):
    """
    Dockable plugin class
    """
    widget_class: Type[PiePluginDockableWidget] = None

    def call(self) -> None:
        self.get_widget().dock_widget()


class PieMediaPlugin(PiePlugin):

    def call(self, index: int, media_file: MediaFile) -> None:
        raise NotImplementedError

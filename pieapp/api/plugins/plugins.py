from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow

from pieapp.api.managers.actions.mixins import ActionAccessorMixin
from pieapp.helpers.logger import logger

from pieapp.api.exceptions import PieException
from pieapp.api.plugins.types import PluginType
from pieapp.api.plugins.observer import PluginsObserverMixin


class PieObject(QObject, PluginsObserverMixin):
    """
    Base object
    """
    # Plugin name
    name: str

    # Plugin type
    type: PluginType = PluginType.Object

    # List of required built-in plugins
    requires: list[str] = []

    # List of optional built-in plugins
    optional: list[str] = []

    # Signal when plugin is ready
    sig_plugin_ready = Signal()

    # Signal when plugin is loading
    sig_plugin_loading = Signal(str)

    # Signal when plugin is reloading
    sig_plugin_reloading = Signal(str)

    # Emit on main window shown
    sig_on_main_window_show = Signal()

    # Emit on main window close
    sig_on_main_window_close = Signal()

    # Signal when exception occurred
    sig_exception_occurred = Signal(PieException)

    def __init__(self, parent: QMainWindow = None, path: Path = None) -> None:
        # Initialize `QObject` instance
        QObject.__init__(self, parent)

        # Initialize `PluginsObserverMixin` instance
        PluginsObserverMixin.__init__(self)

        # Parent object/window
        self._parent = parent

        # PiePlugin path
        self._path: Path = path

        # Just a logger
        self._logger = logger

    @staticmethod
    def get_name() -> str:
        """
        This method returns the translated name of the plugin
        """
        raise NotImplementedError(f"Method \"get_name\" must be implemented")

    @staticmethod
    def get_description() -> str:
        """
        This method returns the translated description of the plugin
        """
        raise NotImplementedError("Method \"get_description\" must be implemented")

    # Prepare methods

    def prepare(self) -> None:
        """
        Prepares the plugin by calling `init` method and emitting `sig_plugin_ready` signal.
        """
        # Initializing plugin
        self.init()

        # Notify that our plugin is ready
        self.sig_plugin_ready.emit()

    # Main methods

    def init(self) -> None:
        """
        Initializes the plugin and required services after forming an instance of the class
        """

    def on_system_shutdown(self) -> None:
        pass

    def before_main_window_visible(self) -> None:
        pass

    def on_main_window_show(self) -> None:
        pass

    def on_main_window_close(self) -> None:
        pass

    def on_close(self) -> None:
        pass

    def can_close(self) -> bool:
        return True

    def get_type(self) -> PluginType:
        return self.type

    def get_path(self) -> Path:
        """
        This method returns the full path of the plugin
        """
        return self._path

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <name: {self.name} type: {self.type.value}>"


class PiePlugin(PieObject, ActionAccessorMixin):
    """
    Base pie-kit plugin
    """
    # Plugin type
    type: PluginType = PluginType.Plugin

    def call(self) -> None:
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
        raise NotImplementedError(f"Method \"get_plugin_icon\" must be implemented")


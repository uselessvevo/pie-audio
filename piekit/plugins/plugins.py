from pathlib import Path

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QMainWindow

from piekit.globals import Global
from piekit.utils.logger import logger
from piekit.plugins.types import PluginType, Error
from piekit.plugins.observer import PluginsObserverMixin


class PiePlugin(
    QObject,
    PluginsObserverMixin,
):
    # Main attributes #

    # Plugin type
    type: PluginType = PluginType.Plugin

    # Plugin codename
    name: str

    # Accessors section
    section: str = None

    # List of required built-in plugins
    requires: list[str] = []

    # List of optional built-in plugins
    optional: list[str] = []

    api: "PiePluginAPI" = None

    # Qt configuration #

    # Signal when plugin is ready
    sig_plugin_ready = Signal()

    # Signal when plugin is loading
    sig_plugin_loading = Signal(str)

    # Signal when plugin is reloading
    sig_plugin_reloading = Signal(str)

    # Signal when main window is closing
    sig_on_main_window_close = Signal()

    # Signal when exception occurred
    sig_exception_occurred = Signal(Error)

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

    # Prepare methods

    def prepare(self) -> None:
        # Initializing plugin
        self.init()

        # Prepare PiePluginAPI
        self.init_api()

        # Notify that our plugin is ready
        self.sig_plugin_ready.emit()

    # Main methods

    def init(self) -> None:
        """
        Initialize an object for the first time.
        For example, you can call managers' register method
        """

    def call(self) -> None:
        """
        Call an object.
        Notice, don't call managers' register methods.
        """
        raise NotImplementedError(f"Method `call` is not implemented")

    def init_api(self) -> None:
        """
        Method that prepare PiePluginAPI based instance
        """
        if self.api:
            self.api = self.api(self)
            self.api.init()

    # Properties

    def get_name(self) -> str:
        return self.name

    def get_path(self) -> Path:
        return self._path

    def get_description(self) -> str:
        return f"{self.name.capitalize()} description"

    def get_plugin_icon(self) -> "QIcon":
        raise NotImplementedError("A plugin icon must be defined")

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <id: {id(self)}, name: {self.name}>"

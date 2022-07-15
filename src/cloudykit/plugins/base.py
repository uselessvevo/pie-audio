import abc
import sys
import inspect
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal

from cloudykit.utils.logger import DummyLogger
from objects.mixins import ManagersRegistry


class Plugin(QObject):
    name: str = None

    """
    Plugin signals:
    
    * signalPluginReady - emit when plugin is ready
    * signalPluginReloadRequested - emit to notify PluginManager to reload plugin
    * signalPluginExceptionOccurred - emit to notify exception handler to handle exception
    """
    signalPluginReady = pyqtSignal()
    signalPluginReloadRequested = pyqtSignal()
    signalPluginExceptionOccurred = pyqtSignal(dict)

    """
    Main window signals:
    
    * signalMainWindowQuit - emit to request main window to quit 
    * signalMainWindowMoved - emitted when the main window is moved
    * signalMainWindowResized - emitted when the main window is resized
    """
    signalRequestMainWindowQuit = pyqtSignal()
    signalMainWindowMoved = pyqtSignal('QMoveEvent')
    signalMainWindowResized = pyqtSignal('QResizeEvent')

    def __init__(self, parent: QObject, *args, **kwargs) -> None:
        super().__init__(parent)

        # Set main attributes
        self.parent = parent
        self.shortcut = None
        self.widget = None

        self.is_registered = False
        # Setting plugin's root like this because we're importing it by `importlib`
        self.root = Path(inspect.getfile((sys.modules.get(self.__class__.__name__)))).parent

        # Setup logger
        self.logger = DummyLogger(self.__class__.__name__)

        self.managers_registry = ManagersRegistry(self)

    @abc.abstractmethod
    def init(self) -> None:
        raise NotImplementedError('Method `init` must be implemented')

    @abc.abstractmethod
    def refresh(self):
        raise NotImplementedError('Method `refresh` must be implemented')

    @abc.abstractmethod
    def mount(self) -> None:
        """ Mount (setup) managers, services, etc. """
        raise NotImplementedError('Method `mount` must be implemented')

    def unmount(self) -> None:
        """ Unmount managers, services, etc. """
        self.managers_registry.unmount()

    def reload(self):
        """ Reload services and refresh widget """
        self.managers_registry.reload()
        self.refresh()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {id(self)} name: {self.name}>'

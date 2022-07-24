import sys
import inspect
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal

from cloudykit.objects.registry import ManagerRegistry
from cloudykit.utils.logger import DummyLogger


class BasePlugin(QObject):
    name: str = None
    config: "BaseConfigPage" = None

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

        # Public attributes
        self.parent = parent
        self.shortcut = None
        self.widget = None
        self.is_registered = False
        # Setting plugin's root like this because we're importing it by `importlib`
        self.root = Path(inspect.getfile((sys.modules.get(self.__class__.__name__)))).parent

        # Private, protected attributes
        self.logger = DummyLogger(self.__class__.__name__)
        self.registry = ManagerRegistry(self, as_mixin=True)

    # Ui methods

    def init(self) -> None:
        """ Method for widget initialization """
        raise NotImplementedError('Method `init` must be implemented')

    def refresh(self):
        """ Refresh widget method """

    # Managers, services methods

    def mount(self) -> None:
        """
        Optional method for mounting managers, services, etc.

        In `Plugin` class we're using string import, because all
        these managers are generic and don't require any additional setup.

        Unless, if you need to do extra preparations for your manager,
        you can import manager right in the `Plugin.mount` method
        and do your thing

        For example:
        >>> from yourapp.registry.cool_manager.manager import CoolManager
        >>> cool_manager = CoolManager()  # creating instance of our manager
        >>> cool_manager.extra_method()  # extra preparation method
        >>> cool_manager.mount()  # basic `mount` method

        But if you're using generic plugins,
        you need to pass import strings into ManagersRegistry's `mount` method

        For example:
        >>> self.registry.mount()
        """

    def unmount(self) -> None:
        """ Optional method for mounting managers, services, etc. """

    # Etc. methods

    def reload(self) -> None:
        """ Predefined method for reloading services and refresh widget """
        self.registry.reload()
        self.refresh()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {id(self)} name: {self.name}>'

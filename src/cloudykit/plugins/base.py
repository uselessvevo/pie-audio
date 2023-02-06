from pathlib import Path

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from cloudykit.system import System
from cloudykit.system.registry import ManagersRegistry

from cloudykit.utils.logger import logger
from cloudykit.system import PathConfig, Error
from cloudykit.plugins.mixins import MenuMixin
from cloudykit.plugins.mixins import ActionMixin
from cloudykit.plugins.observers import PluginObserverMixin
from cloudykit.components.mixins import ComponentMixin


class BasePlugin(
    QObject,
    PluginObserverMixin,
    ActionMixin,
    MenuMixin,
    ComponentMixin,
):
    # Main attributes #

    # Plugin codename
    name: str

    # Icon name
    icon: str = "app.ico"

    # By default, description must be written in English
    description: str

    # Plugin version
    version: tuple[int] = (0, 1, 0)

    # List of required built-in plugins
    requires: list[str] = []

    # List of optional built-in plugins
    optional: list[str] = []
    
    # List of required built-in components
    required_components: list[str]

    # List of optional built-in components
    optional_components: list[str]

    # Qt configuration #

    # Signal when plugin is ready
    signalPluginReady = pyqtSignal()
    
    # Signal when plugin is loading
    signalPluginLoading = pyqtSignal(str)
    
    # Signal when plugin is reloading
    signalPluginReloading = pyqtSignal(str)

    # Signal when main window is closing
    signalOnMainWindowClose = pyqtSignal()
    
    # Signal when exception occurred
    signalExceptionOccurred = pyqtSignal(Error)

    def __init__(
        self,
        parent: QObject = None,
        path: Path = None,
    ) -> None:
        super().__init__(parent)

        # Just a logger
        self._logger = logger

        # Parent object/window
        self._parent = parent

        # Plugin path
        self._path: Path = path

        self._managers: list["BaseMager"] = []

        # Flag: is plugin registered
        self._is_registered: bool = False

    # Main methods

    def mount(self) -> None:
        """
        Mount managers method

        Attention! You need to add manager's name into `_managers` list
        """
        if (self._path / System.config.CONFIGS_FOLDER).exists():
            System.registry.configs.mount(PathConfig(self._path, section=self.name))
            self._managers.append(System.registry.configs.name)

        if (self._path / System.config.LOCALES_FOLDER).exists():
            System.registry.locales.mount(PathConfig(self._path, section=self.name))
            self._managers.append(System.registry.locales.name)

        if (self._path / System.config.ASSETS_FOLDER).exists():
            System.registry.assets.mount(PathConfig(self._path, section=self.name))
            self._managers.append(System.registry.assets.name)

    def unmount(self) -> None:
        """ Unmount managers by list of managers """
        for manager in self._managers:
            manager_inst = System.registry.get(manager)
            if manager_inst:
                manager_inst.delete(self.name)

    def prepare(self) -> None:
        # First, we need to initialize base signals
        self.prepareBaseSignals()

        # Plugin is loading
        self.signalPluginLoading.emit(self.__class__.__name__)

        # Prepare managers
        self.mount()

        # Render on MainWindow's or other plugin components
        self.renderOnParent()

        # Plugin is ready
        self.signalPluginReady.emit()

        # Inform about that
        self.logger.info(f"Plugin {self.name} is ready!")

    # Signals, shortcuts etc. methods

    def prepareBaseSignals(self):
        self.logger.info(f"Preparing base signals for {self.__class__.__name__}")
        # self.signalPluginReady.connect(self._parent.signalPluginReady)
        self.signalPluginLoading.connect(self._parent.signalPluginLoading)
        self.signalPluginReloading.connect(self._parent.signalPluginReloading)
        self.signalExceptionOccurred.connect(self.errorHandler)

    def prepareShortcuts(self) -> None:
        """ Prepare plugin's shortcuts and register them in `ShortcutsManager` """
        pass

    def prepareConfigurationPage(self) -> None:
        """ Prepare configuration page widget """
        pass

    # Render methods

    def renderOnParent(self) -> None:
        """ Render plugin on parent's component """
        pass

    def init(self) -> None:
        """ Render object window """
        raise NotImplementedError("Method `call` must be implemented")

    # Update methods

    def updateStyle(self) -> None:
        pass

    def updateLocalization(self) -> None:
        pass

    # Event methods

    def onShow(self, *args, **kwargs) -> None:
        pass

    def show(self) -> None:
        self.onShow()
        super().show()

    def onCloseEvent(self) -> None:
        self.logger.info("Closing. Goodbye!..")

    # Getter methods

    def getTitle(self) -> str:
        version = ".".join(str(i) for i in self.version)
        return f"{self.name} • {version}"

    def getName(self) -> str:
        return self.name or self.__class__.__name__

    def getDescription(self) -> str:
        return self.description or f"{self.__class__.__class__}'s description"

    def getVersion(self) -> tuple[int]:
        return self.version

    def getIcon(self) -> str:
        return System.registry.assets.get(self.icon)

    # Signals

    @pyqtSlot(Error)
    def errorHandler(self, error: Error) -> None:
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Critical)
        messageBox.setText(error.title)
        messageBox.setInformativeText(error.description)
        messageBox.setWindowTitle(System.registry.locales("shared", "Error"))
        messageBox.exec_()

    # Properties

    @property
    def logger(self):
        return self._logger

    @property
    def registry(self) -> ManagersRegistry:
        return System.registry

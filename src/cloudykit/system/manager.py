from pathlib import Path

from PyQt5.QtCore import QObject

from cloudykit.objects.logger import logger
from cloudykit.system.loader import ConfigLoader
from cloudykit.system.registry import ManagersRegistry


class SystemManager(QObject):
    """ Simple manager that provides access to """

    def __init__(self) -> None:
        super().__init__(parent=None)

        self._logger = logger
        self._config = ConfigLoader()
        self._root = self.config.APP_ROOT
        self._registry = ManagersRegistry(self)

    def mount(self) -> None:
        """
        Read configs and check if all required configs are in directory
        """
        self._registry.mount(*System.config.MANAGERS)
        self._logger.info("All Systems Nominal")

    def unmount(self) -> None:
        self._registry.unmount()
        self._logger.info("Goodbye!")

    @property
    def config(self) -> ConfigLoader:
        return self._config

    @property
    def registry(self) -> ManagersRegistry:
        return self._registry

    @property
    def logger(self) -> logger:
        return self._logger

    @property
    def root(self):
        return self._root


System = SystemManager()

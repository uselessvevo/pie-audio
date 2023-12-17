from typing import Union, Type
from pathlib import Path

from piekit.helpers.logger import logger
from piekit.helpers.files import read_json
from piekit.helpers.modules import import_by_string
from piekit.managers.base import BaseManager


class ManagersRegistry:

    def __init__(self) -> None:
        # Just a logger
        self._logger = logger

        # Dictionary with base managers
        self._managers_instances: dict[str, BaseManager] = {}

    def from_class(self, manager_class: Type[BaseManager]) -> None:
        """
        Initialize manager manualy. Pass manager class (not an instance) with args and kwargs
        For example:
        >>> from piekit.managers.registry import Managers
        >>> from piekit.managers.configs.manager import ConfigManager
        >>> Managers.init(ConfigManager, PathConfig(...), ...)
        """
        manager_instance = manager_class()
        self._managers_instances[manager_instance.name] = manager_instance
        self._logger.info(f"Initializing \"{manager_instance.__class__.__name__}\"")
        manager_instance.init()

    def from_string(self, import_string: str) -> None:
        """
        Initialize manager from import string
        """
        manager_instance = import_by_string(import_string)()
        self._managers_instances[manager_instance.name] = manager_instance
        self._logger.info(f"Initializing \"{manager_instance.__class__.__name__}\"")
        manager_instance.init()

    def from_json(self, file: Union[str, Path]) -> None:
        """
        Initialize managers from json file.
        File structure must have an array with the next parameters
            * import_string (str): import string separated by dots - 'path.to.manager.ManagerClassName'

        For example: <import string>, ...]`
        """
        file_data = read_json(file)
        file_data = tuple(fd["import"] for fd in file_data)

        for config in file_data:
            self.from_string(config)

    def shutdown(self, *managers: str, full_house: bool = False) -> None:
        self._logger.info("Preparing to shutdown all managers")
        managers = reversed(self._managers_instances.keys()) if full_house else managers
        managers_instances = (self._managers_instances.get(i) for i in managers or self._managers_instances.keys())

        for manager_instance in managers_instances:
            self._logger.info(f"Shutting down \"{manager_instance.__class__.__name__}\"")
            manager_instance.shutdown(full_house=True)

    def reload(self, *managers: tuple[BaseManager], full_house: bool = False):
        managers = reversed(self._managers_instances.keys()) if full_house else managers
        managers_instances = (self._managers_instances.get(i) for i in managers)

        for manager_instance in managers_instances:
            self._logger.info(f"Reloading \"{manager_instance.__class__.__name__}\"")
            manager_instance.reload()

    def destroy(self, *managers: str, full_house: bool = False):
        managers = reversed(self._managers_instances.keys()) if full_house else managers

        for manager in managers:
            self._logger.info(f"Destroying \"{manager.__class__.__name__}\"")
            self._managers_instances.pop(manager)

    def __call__(self, manager: str, fallback_method: callable = None) -> BaseManager:
        """
        Call needed manager instance via its name
        For example: `Managers(SysManager.Configs).get(...)`
        
        Args:
            manager (str): manager instance name
            fallback_method (callable): method to call if manager was not found

        Returns:
            BaseManager instance
        """
        try:
            return self._managers_instances[manager]
        except AttributeError:
            if not fallback_method:
                raise AttributeError(f"Manager \"{manager}\" not found or not initialized")

            fallback_method()


Managers = ManagersRegistry()

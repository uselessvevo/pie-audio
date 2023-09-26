from typing import Union, Type
from pathlib import Path

from piekit.utils.logger import logger
from piekit.utils.files import read_json
from piekit.utils.modules import import_by_string
from piekit.managers.base import PluginBaseManager, BaseManager
from piekit.managers.structs import ManagerConfig


class ManagersRegistry:

    def __init__(self) -> None:
        # Just a logger
        self._logger = logger

        # Dictionary with base managers
        self._managers_instances: dict[str, BaseManager] = {}

        # Dictionary with managers that can setup plugins
        self._plugin_managers_instances: dict[str, PluginBaseManager] = {}

    def from_class(self, manager_class: Type[BaseManager], init: bool = True, *args, **kwargs) -> None:
        """
        Initialize manager manualy. Pass manager class (not an instance) with args and kwargs
        For example:
        >>> from piekit.managers.registry import Managers
        >>> from piekit.managers.configs.manager import ConfigManager
        >>> Managers.init(ConfigManager, PathConfig(...), ...)
        """
        manager_instance = manager_class()
        self._logger.info(f"Initializing \"{manager_instance.__class__.__name__}\"")

        self._managers_instances[manager_instance.name] = manager_instance
        if isinstance(manager_instance, PluginBaseManager):
            self._plugin_managers_instances[manager_instance.name] = manager_instance

        setattr(self, manager_instance.name, manager_instance)

        if init is True:
            manager_instance.init(*args, **kwargs)

        setattr(manager_instance, "ready", init)

    def from_config(self, config: ManagerConfig) -> None:
        """
        Initialize manager from `ManagerConfig` structure
        """
        manager_instance = import_by_string(config.import_string)()
        self._logger.info(f"Initializing \"{manager_instance.__class__.__name__}\"")

        self._managers_instances[manager_instance.name] = manager_instance
        if isinstance(manager_instance, PluginBaseManager):
            self._plugin_managers_instances[manager_instance.name] = manager_instance
            
        setattr(self, manager_instance.name, manager_instance)

        if config.init is True:
            manager_instance.init(*config.args, **config.kwargs)

        setattr(manager_instance, "ready", config.init)

    def from_json(self, file: Union[str, Path]) -> None:
        """
        Initialize managers from json file.
        File structure must have an array with the next parameters
            * import_string (str): import string separated by dots - 'path.to.manager.ManagerClassName'
            * init (bool): initialize manager

        For example: `[{"import_string": string, "init": boolean}, ...]`
        """
        file_data = read_json(file)
        file_data = tuple(ManagerConfig(import_string=f["import"], init=file["init"]) for f in file_data)

        for config in file_data:
            self.from_config(config)

    def shutdown(self, *managers: str, full_house: bool = False) -> None:
        self._logger.info("Preparing to shutdown all managers")
        managers = reversed(self._managers_instances.keys()) if full_house else managers
        managers_instances = (self._managers_instances.get(i) for i in managers or self._managers_instances.keys())

        for manager_instance in managers_instances:
            self._logger.info(f"Shutting down \"{manager_instance.__class__.__name__}\" "
                              f"from \"{self.__class__.__name__}\"")
            manager_name = manager_instance.name
            if isinstance(manager_instance, PluginBaseManager):
                manager_instance.shutdown_plugin()

            manager_instance.shutdown(full_house=True)
            delattr(self, manager_name)

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
            delattr(self, manager)

    def get_plugin_managers(self) -> list[PluginBaseManager]:
        return list(self._plugin_managers_instances.values())

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
            return self.__getattribute__(manager)
        except AttributeError:
            if not fallback_method:
                raise AttributeError(f"Manager \"{manager}\" not found or not initialized")

            fallback_method()


Managers = ManagersRegistry()

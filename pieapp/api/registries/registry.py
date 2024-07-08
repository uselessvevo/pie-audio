from typing import Type

from pieapp.helpers.logger import logger
from pieapp.helpers.modules import import_by_string
from pieapp.api.registries.base import BaseRegistry


class RegistryContainer:

    def __init__(self) -> None:
        # Dictionary of `BaseRegistry` based classes
        self._managers_instances: dict[str, BaseRegistry] = {}

    def init_from_class(self, manager_class: Type[BaseRegistry]) -> None:
        """
        Initialize manager manualy. Pass manager class (not an instance) with args and kwargs
        For example:
        >>> from pieapp.api.managers.registry import Registry
        >>> from pieapp.api.managers.configs.manager import ConfigRegistry
        >>> Registry.init(ConfigRegistry, PathConfig(...), ...)
        """
        manager_instance = manager_class()
        self._managers_instances[manager_instance.name] = manager_instance
        logger.debug(f"Initializing \"{manager_instance.__class__.__name__}\"")
        manager_instance.init()

    def init_from_string(self, import_string: str) -> None:
        """
        Initialize manager from import string
        """
        manager_instance = import_by_string(import_string)()
        self._managers_instances[manager_instance.name] = manager_instance
        logger.debug(f"Initializing \"{manager_instance.__class__.__name__}\"")
        manager_instance.init()

    def restore(self, *managers: tuple[BaseRegistry], all_managers: bool = False):
        managers = reversed(self._managers_instances.keys()) if all_managers else managers
        managers_instances = (self._managers_instances.get(i) for i in managers)
        for manager_instance in managers_instances:
            logger.debug(f"Restoring \"{manager_instance.__class__.__name__}\"")
            manager_instance.restore()

    def reload(self, *managers: tuple[BaseRegistry], all_managers: bool = False):
        managers = reversed(self._managers_instances.keys()) if all_managers else managers
        managers_instances = (self._managers_instances.get(i) for i in managers)
        for manager_instance in managers_instances:
            logger.debug(f"Reloading \"{manager_instance.__class__.__name__}\"")
            manager_instance.reload()

    def __call__(self, manager: str, fallback_method: callable = None) -> BaseRegistry:
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


Registry = RegistryContainer()

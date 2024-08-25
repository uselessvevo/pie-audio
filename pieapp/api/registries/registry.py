from typing import Type

from pieapp.utils.logger import logger
from pieapp.utils.modules import import_by_string
from pieapp.api.registries.base import BaseRegistry


class RegistryContainer:

    def __init__(self) -> None:
        # Dictionary of `BaseRegistry` based classes
        self._managers_instances: dict[str, BaseRegistry] = {}

    def init_from_class(self, manager_class: Type[BaseRegistry]) -> None:
        """
        Initialize manager manualy. Pass manager class (not an instance) with args and kwargs
        For example:
        >>> from pieapp.api.registries.registry import Registry
        >>> from pieapp.api.registries.configs.manager import ConfigRegistry
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
        manager_instance = import_by_string(import_string)
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


Registry = RegistryContainer()

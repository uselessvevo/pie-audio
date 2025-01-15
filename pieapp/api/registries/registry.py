from typing import Type

from pieapp.api.utils.logger import logger
from pieapp.api.utils.modules import import_by_string
from pieapp.api.registries.base import BaseRegistry


class _RegistryContainer:

    def __init__(self) -> None:
        # Dictionary of `BaseRegistry` based instances
        self._registries: dict[str, BaseRegistry] = {}

    def init_from_class(self, registry_class: Type[BaseRegistry]) -> None:
        """
        Initialize registry manualy. Pass registry class (not an instance) with args and kwargs
        For example:
        >>> from pieapp.api.registries.registry import RegistryContainer
        >>> from pieapp.api.registries.configs.registry import ConfigRegistry
        >>> RegistryContainer.init_from_class(ConfigRegistry)
        """
        registry_instance = registry_class()
        self._registries[registry_instance.name] = registry_instance
        logger.debug(f"Initializing \"{registry_instance.__class__.__name__}\"")
        registry_instance.init()

    def init_from_string(self, import_string: str) -> None:
        """
        Initialize registry from import string
        """
        registry_instance = import_by_string(import_string)
        self._registries[registry_instance.name] = registry_instance
        logger.debug(f"Initializing \"{registry_instance.__class__.__name__}\"")
        registry_instance.init()

    def shutdown(self, *registries: tuple[BaseRegistry], all_registries: bool = False):
        registries = reversed(self._registries.keys()) if all_registries else registries
        registries_instances = (self._registries.get(i) for i in registries)
        for registry_instance in registries_instances:
            logger.debug(f"Restoring \"{registry_instance.__class__.__name__}\"")
            registry_instance.destroy()

    def restore(self, *registries: tuple[BaseRegistry], all_registries: bool = False):
        registries = reversed(self._registries.keys()) if all_registries else registries
        registries_instances = (self._registries.get(i) for i in registries)
        for registry_instance in registries_instances:
            logger.debug(f"Restoring \"{registry_instance.__class__.__name__}\"")
            registry_instance.restore()

    def reload(self, *registries: tuple[BaseRegistry], all_registries: bool = False):
        registries = reversed(self._registries.keys()) if all_registries else registries
        registries_instances = (self._registries.get(i) for i in registries)
        for registry_instance in registries_instances:
            logger.debug(f"Reloading \"{registry_instance.__class__.__name__}\"")
            registry_instance.reload()

    def get_registry(self, registry_name: str) -> BaseRegistry:
        return self._registries.get(registry_name, None)


RegistryContainer = _RegistryContainer()

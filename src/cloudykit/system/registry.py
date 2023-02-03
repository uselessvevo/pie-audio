from typing import Union

from cloudykit.utils.logger import logger
from cloudykit.managers.base import BaseManager
from cloudykit.system.types import ManagerConfig
from cloudykit.utils.modules import import_by_string
from cloudykit.system.exceptions import ObjectNotMountedError, DependencyNotFoundError


class ManagersRegistry:

    def __init__(self, parent) -> None:
        # SystemManager
        self._parent = parent

        # Just a logger
        self._logger = logger
        
        # Set with stored `BaseManager` base classes. Use to reload them
        self._managers_instances: dict[str, BaseManager] = {}
        
    def _check_dependencies(self, obj):
        """
        Checks required managers to be mounted in `System.registry`
        """
        for dependency in getattr(obj, "dependencies") or tuple():
            self._logger.info(f"Checking {obj.__class__.__name__} manager dependencies")
            managers = tuple(i.import_string.split(".")[2] for i in self._parent.config.MANAGERS)

            if dependency not in managers and not hasattr(self, dependency):
                raise DependencyNotFoundError(dependency)

            if dependency in managers and not self._is_mounted(dependency):
                # TODO: Add managers order resolver
                raise ObjectNotMountedError(dependency)

    def _mount_manually(self, manager: BaseManager, *args, **kwargs) -> None:
        """ 
        Mount manager manualy. Pass manager class (not an instance) with args and kwargs
        
        For example:
        >>> from cloudykit.system.manager import System
        >>> from cloudykit.managers.configs.manager import ConfigManager
        >>> System.mount()
        >>> System.registry.mount(ConfigManager, PathConfig(...), ...)
        """
        manager = manager(self._parent)
        self._check_dependencies(manager)
        self._logger.info(f"Mounting `{manager.__class__.__name__}` in `{self._parent.__class__.__name__}`")

        manager.mount(*args, **kwargs)
        self._managers_instances[manager.name] = manager

        setattr(self, manager.name, manager)
        setattr(manager, "mounted", True)

    def _mount_from_config(self, config: ManagerConfig) -> None:
        """ Mount manager from dictionary """
        manager_instance = import_by_string(config.import_string)(self._parent)
        self._check_dependencies(manager_instance)
        
        self._logger.info(f"Mounting `{manager_instance.__class__.__name__}` in `{self._parent.__class__.__name__}`")
        if config.mount is True:
            manager_instance.mount(*config.args, **config.kwargs)

        self._managers_instances[manager_instance.name] = manager_instance
        setattr(self, manager_instance.name, manager_instance)
        setattr(manager_instance, "mounted", config.mount)

    def mount(self, *managers: Union[ManagerConfig, BaseManager]) -> None:
        """
        Mount (add) managers by import string or instance of manager
        For example:
        >>> self.registry = ManagersRegistry()
        >>> self.registry.mount()
        """
        for manager in managers:
            if isinstance(manager, ManagerConfig):
                self._mount_from_config(manager)

            elif issubclass(manager, BaseManager):
                self._mount_manually(manager)

            else:
                self._logger.info(f"Manager {manager} has incorrect `{type(manager)}` type. Skipping.")
                continue

    def unmount(self, *managers: str, full_house: bool = False) -> None:
        self._logger.info("Preparing to unmount all managers")
        managers = reversed(self._managers_instances.keys()) if full_house else managers
        managers_instances = [self._managers_instances.get(i) for i in managers or self._managers_instances.keys()]

        for manager_instance in managers_instances:
            self._logger.info(f"Unmounting `{manager_instance.__class__.__name__}` from `{self.__class__.__name__}`")
            manager_name = manager_instance.name
            manager_instance.unmount(full_house=True)
            delattr(self, manager_name)

    def reload(self, *managers: tuple[BaseManager], full_house: bool = False):
        managers = reversed(self._managers_instances.keys()) if full_house else managers
        managers_instances = [self._managers_instances.get(i) for i in managers]

        for manager_instance in managers_instances:
            self._logger.info(f"Reloading `{manager_instance.__class__.__name__}`")
            manager_instance.reload()

    def destroy(self, *managers: str, full_house: bool = False):
        managers = reversed(self._managers_instances.keys()) if full_house else managers

        for manager in managers:
            self._logger.info(f"Destroying `{manager.__class__.__name__}`")
            delattr(self, manager)

    def _is_mounted(self, name: str) -> bool:
        manager = getattr(self, name)
        return manager.mounted

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            raise ObjectNotMountedError(item)

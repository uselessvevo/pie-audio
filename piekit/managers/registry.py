from typing import Union

from piekit.utils.logger import logger
from piekit.managers.base import BaseManager
from piekit.managers.structs import ManagerConfig
from piekit.config import Config
from piekit.utils.modules import import_by_string
from piekit.managers.exceptions import ManagerNotReadyError, DependencyNotFoundError


class ManagersRegistry:

    def __init__(self) -> None:
        # Just a logger
        self._logger = logger

        # Dictionary with stored `BaseManager` base classes. Use to reload them
        self._managers_instances: dict[str, BaseManager] = {}

    def _check_dependencies(self, obj):
        """
        Checks required managers
        """
        for dependency in getattr(obj, "dependencies") or tuple():
            self._logger.info(f"Checking {obj.__class__.__name__} manager dependencies")
            managers = tuple(i.import_string.split(".")[2] for i in Config.MANAGERS)

            if dependency not in managers and not hasattr(self, dependency):
                raise DependencyNotFoundError(dependency)

            if dependency in managers and not self._is_ready(dependency):
                # TODO: Add managers order resolver
                raise ManagerNotReadyError(dependency)

    def _init_manually(self, manager: BaseManager, *args, **kwargs) -> None:
        """ 
        Initialize manager manualy. Pass manager class (not an instance) with args and kwargs

        For example:
        >>> from piekit.managers.registry import Managers
        >>> from piekit.managers.configs.manager import ConfigManager
        >>> Managers.init(ConfigManager, PathConfig(...), ...)
        """
        manager = manager()
        self._check_dependencies(manager)
        self._logger.info(f"Initializing `{manager.__class__.__name__}`")

        manager.init(*args, **kwargs)
        self._managers_instances[manager.name] = manager

        setattr(self, manager.name, manager)
        setattr(manager, "ready", True)

    def _init_from_config(self, config: ManagerConfig) -> None:
        """
        Initialize manager from `ManagerConfig` structure
        """
        manager_instance = import_by_string(config.import_string)()
        self._check_dependencies(manager_instance)

        self._logger.info(f"Initializing `{manager_instance.__class__.__name__}`")
        if config.init is True:
            manager_instance.init(*config.args, **config.kwargs)

        self._managers_instances[manager_instance.name] = manager_instance
        setattr(self, manager_instance.name, manager_instance)
        setattr(manager_instance, "ready", config.init)

    def init(self, *managers: Union[ManagerConfig, BaseManager]) -> None:
        """
        Add and initialize managers via import string or via `BaseManager` instance
        >>> Managers.init(*Config.MANAGERS)
        """
        for manager in managers:
            if isinstance(manager, ManagerConfig):
                self._init_from_config(manager)

            elif issubclass(manager, BaseManager):
                self._init_manually(manager)

            else:
                self._logger.info(f"Manager {manager} has incorrect `{type(manager)}` type. Skipping.")
                continue

    def shutdown(self, *managers: str, full_house: bool = False) -> None:
        self._logger.info("Preparing to shutdown all managers")
        managers = reversed(self._managers_instances.keys()) if full_house else managers
        managers_instances = [self._managers_instances.get(i) for i in managers or self._managers_instances.keys()]

        for manager_instance in managers_instances:
            self._logger.info(f"Shutting down `{manager_instance.__class__.__name__}` from `{self.__class__.__name__}`")
            manager_name = manager_instance.name
            manager_instance.shutdown(full_house=True)
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

    def _is_ready(self, name: str) -> bool:
        manager = getattr(self, name)
        return manager.ready

    def get(self, manager: str) -> BaseManager:
        try:
            return self.__getattribute__(manager)
        except AttributeError:
            raise ManagerNotReadyError(manager)

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def __getattr__(self, *args, **kwargs) -> BaseManager:
        return self.get(*args, **kwargs)


Managers = ManagersRegistry()

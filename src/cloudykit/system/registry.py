from typing import Union

from cloudykit.objects.logger import logger
from cloudykit.objects.manager import BaseManager
from cloudykit.utils.modules import import_by_string
from cloudykit.system.exceptions import ObjectNotMountedError, DependencyNotFoundError


class ManagersRegistry:

    def __init__(self, parent) -> None:
        self._parent = parent
        
        # Set with stored `BaseManager` base classes. Use to reload them
        self._managers_instances: list[BaseManager] = []
        
        # Just a logger
        self._logger = logger

    def _check_dependencies(self, obj):
        """
        Checks required objects to be mounted in `System.registry`
        """
        for dependency in getattr(obj, "dependencies") or tuple():
            self._logger.info(f"Checking {obj.__class__.__name__} manager dependencies")
            managers = tuple(i.get("import").split(".")[2] for i in self._parent.config.MANAGERS)

            if dependency not in managers and not hasattr(self, dependency):
                raise DependencyNotFoundError(dependency)

            if dependency in managers and not self._is_mounted(dependency):
                # TODO: Add managers order resolver
                raise ObjectNotMountedError(dependency)

    def _mount_from_object(self, manager: BaseManager) -> None:
        """ 
        Mount manager manualy
        
        For example:
        >>> from cloudykit.system.manager import System
        >>> from cloudykit.managers.userconfigs.manager import UserConfigsManager
        >>> System.mount()
        >>> System.registry.mount()
        """
        self._logger.info(f"Mounting `{manager.__class__.__name__}` in `{self._parent.__class__.__name__}`")

        manager = manager(self._parent)
        self._check_dependencies(manager)
        manager.mount()
        self._managers_instances.append(manager)

        setattr(self, manager.__class__.__name__.lower().replace("manager", ""), manager)
        setattr(manager, "mounted", True)

    def _mount_from_string(self, manager: str) -> None:
        """ Mount from import string """
        manager_name = manager.split(".")[-3]
        manager_inst = import_by_string(manager)(self._parent)
        self._logger.info(f"Mounting `{manager_inst.__class__.__name__}` in `{self._parent.__class__.__name__}`")

        self._check_dependencies(manager_inst)
        manager_inst.mount()
        self._managers_instances.append(manager_inst)

        setattr(self, manager_name, manager_inst)
        setattr(manager_inst, 'mounted', True)

    def _mount_from_dict(self, manager: dict) -> None:
        """ Mount manager from dictionary """
        manager_name = manager.get("import").split(".")[-3]
        manager_inst = import_by_string(manager.get("import"))(self._parent)
        self._check_dependencies(manager_inst)
        
        self._logger.info(f"Mounting `{manager_inst.__class__.__name__}` in `{self._parent.__class__.__name__}`")
        if manager.get("mount") is True:
            manager_inst.mount()

        self._managers_instances.append(manager_inst)
        setattr(self, manager_name, manager_inst)
        setattr(manager_inst, 'mounted', True)

    def mount(self, *managers: Union[tuple[str], tuple[BaseManager]]) -> None:
        """
        Mount (add) managers by import string or instance of manager
        For example:
        >>> self.registry = ManagersRegistry()
        >>> self.registry.mount()
        """
        for manager in managers:
            if isinstance(manager, str):
                self._mount_from_string(manager)

            elif isinstance(manager, dict):
                self._mount_from_dict(manager)

            elif issubclass(manager, BaseManager):
                self._mount_from_object(manager)

            else:
                self._logger.info(f"Object {manager} is not a valid object. Skipping...")
                continue

    def unmount(self, *managers: tuple[BaseManager]) -> None:
        self._logger.info("Preparing to unmount all managers")
        managers_instances = managers or self._managers_instances

        for manager_instance in managers_instances:
            self._logger.info(f"Unmounting `{manager_instance.__class__.__name__}` from `{self.__class__.__name__}`")
            manager_name = manager_instance.__class__.__name__.lower().replace("manager", "")
            manager_instance.unmount()
            delattr(self, manager_name)

    def reload(self, *managers: tuple[BaseManager], full_house: bool = False):
        managers = self._managers_instances if full_house else set(*managers)

        for manager_inst in managers:
            self._logger.info(f"Reloading ""{manager_inst.__class__.__name__}""")
            manager_inst.unmount()
            manager_inst.mount()

    def destroy(self, *managers: tuple[BaseManager]):
        managers = set(*managers)

        for manager_inst in managers:
            self._logger.info(f"Destroying `{manager_inst.__class__.__name__}`")
            delattr(self, manager_inst)

    def _is_mounted(self, name: str) -> bool:
        manager = getattr(self, name)
        return manager.mounted

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            raise ObjectNotMountedError(item)

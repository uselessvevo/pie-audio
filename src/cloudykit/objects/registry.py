from typing import List, Set, Tuple, Union

from cloudykit.abstracts.manager import IManager
from cloudykit.utils.modules import import_by_string
from cloudykit.utils.logger import DummyLogger


logger = DummyLogger('ManagersRegistry')


class ManagersRegistry:

    def __init__(
        self,
        parent,
        managers: List[str] = None,
        as_mixin: bool = False
    ) -> None:
        self._parent = parent
        self._as_mixin = as_mixin
        self._managers_inst_set: Set[IManager] = set()
        self._managers_names_set: Set[str] = set(managers or [])

    def _mount_from_string(self, parent, manager: str) -> None:
        manager_inst = import_by_string(manager)()
        logger.log(f'Mounting "{manager_inst.__class__.__name__}" to "{self._parent.__class__.__name__}"')
        manager_inst.mount(self._parent)
        self._managers_inst_set.add(manager_inst)
        setattr(parent, manager_inst.name, manager_inst)

    def _mount_from_class(self, parent, manager_inst: IManager) -> None:
        manager_inst.mount(self._parent)
        logger.log(f'Mounting "{manager_inst.__class__.__name__}" to "{self._parent.__class__.__name__}"')
        self._managers_inst_set.add(manager_inst)
        setattr(parent, manager_inst.name, manager_inst)

    def _mount_from_dict(self, parent, manager: dict) -> None:
        manager_inst = import_by_string(manager.get('import'))()
        logger.log(f'Mounting "{manager_inst.__class__.__name__}" to "{self._parent.__class__.__name__}"')
        if manager.get('mount') is True:
            manager_inst.mount(self._parent)

        self._managers_inst_set.add(manager_inst)
        setattr(parent, manager_inst.name, manager_inst)

    def mount(self, *managers: Union[Tuple[str], Tuple[IManager]]) -> None:
        """
        Mount (add) managers by import string or instance of manager
        For example:
        >>> self.registry.mount('path.to.manager.ManagerClass')
        >>> self.managers_regsitry.mount(ManagerClass())
        """
        parent = self if self._as_mixin else self._parent

        for manager in managers:
            if isinstance(manager, str):
                self._mount_from_string(parent, manager)
            elif isinstance(manager, IManager):
                self._mount_from_class(parent, manager)
            elif isinstance(manager, dict):
                self._mount_from_dict(parent, manager)
            else:
                logger.log(f'Object {manager} is not a valid object. Skipping...')
                continue

    def unmount(self, *managers: Tuple[IManager]) -> None:
        parent = self if self._as_mixin else self._parent
        managers = set(*managers)

        for manager_inst in managers:
            manager_inst.unmount(self._parent)
            logger.log(f'Unmounting "{self.__class__.__name__}" to {manager_inst.__class__.__name__}')
            delattr(parent, manager_inst.name)

    def reload(self, *managers: Tuple[IManager]):
        managers = set(*managers)

        for manager_inst in managers:
            logger.log(f'Reloading ""{manager_inst.__class__.__name__}""')
            manager_inst.reload()

    def destroy(self, *managers: Tuple[IManager]):
        managers = set(*managers)

        for manager_inst in managers:
            logger.log(f'Reloading ""{manager_inst.__class__.__name__}""')
            manager_inst.destroy()

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError as e:
            return None

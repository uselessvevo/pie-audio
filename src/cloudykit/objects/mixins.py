from typing import List, Set, Tuple, Union

from cloudykit.abstracts.manager import IManager
from cloudykit.utils.modules import import_by_string


class ManagersRegistry:

    def __init__(self, parent, managers: List[str] = None):
        self._parent = parent
        self._managers_inst_set: Set[IManager] = set()
        self._managers_names_set: Set[str] = set(managers or [])

    def mount(self, *managers: Union[Tuple[str], Tuple[IManager]]) -> None:
        managers = set(managers)

        for manager in managers:
            self._parent.logger.log(f'Mounting "{self.__class__.__name__}" to {manager}')
            if isinstance(manager, str):
                manager_inst = import_by_string(manager)()
            elif isinstance(manager, IManager):
                manager_inst = manager
            else:
                self._parent.logger.log(f'Object {manager} is not a valid object. Skipping...')
                continue

            manager_inst.mount(self._parent)
            self._managers_inst_set.add(manager_inst)
            setattr(self._parent, manager_inst.name, manager_inst)

    def unmount(self, *managers: Tuple[IManager]) -> None:
        managers = set(*managers)

        for manager_inst in managers:
            manager_inst.unmount(self._parent)
            self._parent.logger.log(f'Unmounting "{self.__class__.__name__}" to {manager_inst.__class__.__name__}')
            delattr(self._parent, manager_inst.name)

    def reload(self, *managers: Tuple[IManager]):
        managers = set(*managers)

        for manager_inst in managers:
            self._parent.logger.log(f'Reloading "{manager_inst.name}"')
            manager_inst.reload()

    def destroy(self, *managers: Tuple[IManager]):
        managers = set(*managers)

        for manager_inst in managers:
            self._parent.logger.log(f'Reloading "{manager_inst.name}"')
            manager_inst.destroy()

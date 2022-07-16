import inspect
from functools import lru_cache
from pathlib import Path
from typing import List, Set

from cloudykit.abstracts.manager import IManager
from cloudykit.utils.modules import import_by_path


class SystemManagersRegistry:

    def __init__(self) -> None:
        self._managers: set = self.get_all_managers()

    @lru_cache
    def get_all_managers(self, root: str = None) -> Set[IManager]:
        collect = set()
        root = Path(__file__).parent or Path(root)
        for manager_dir in root.iterdir():
            if manager_dir.is_dir() and manager_dir.name not in ('__pycache__', 'system'):
                manager_mod = import_by_path('manager', str(manager_dir / 'manager.py'))
                manager_members = inspect.getmembers(manager_mod)
                manager_inst = [i for i in manager_members if isinstance(i[1], IManager)]
                if manager_inst:
                    collect.add(manager_inst[0][1])

        return collect

    def destroy(self, managers: List[IManager] = None) -> None:
        """ Destroy managers """
        managers = managers or self._managers
        for manager in managers:
            manager.destroy()

    def reload(self, managers: List[IManager] = None) -> None:
        """ Reload managers """
        managers = managers or self._managers
        for manager in managers:
            manager.reload()

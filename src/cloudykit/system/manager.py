"""
System manager contains:
* AbstractManager based objects
* Configuration from `$APP/configs/*.json`
"""
from pathlib import Path
from typing import Any, List
from dotty_dict import Dotty

from cloudykit.utils.logger import DummyLogger
from cloudykit.objects.mixins import ManagersRegistry


class SystemManager:
    """ Simple manager that provides access to """
    name = 'system'

    def __init__(self) -> None:
        # Private attrs
        self._root: Path = None
        self._config: Dotty = Dotty({})

        # Public attrs
        self.managers_registry = ManagersRegistry(self)
        self.logger = DummyLogger('SystemManager')

        super().__init__()

    def mount(self, root: str) -> None:
        self._root = Path(root)

    @property
    def root(self):
        return self._root


System = SystemManager()

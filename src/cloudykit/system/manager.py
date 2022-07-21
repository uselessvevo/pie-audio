"""
System manager contains:
* AbstractManager based objects
* Configuration from `$APP/configs/*.json`
"""
from pathlib import Path
from dotty_dict import Dotty

from cloudykit.objects.registry import ManagersRegistry
from cloudykit.utils.logger import DummyLogger


class SystemManager:
    """ Simple manager that provides access to """
    name = 'system'

    def __init__(self) -> None:
        # Protected/privdate attrs
        self._root: Path = None
        self._config: Dotty = Dotty({})

        # Public attrs
        self.registry = ManagersRegistry(self)
        self.logger = DummyLogger(self.__class__.__name__)

        super().__init__()

    def mount(self, root: str) -> None:
        self._root = Path(root)

    @property
    def root(self):
        return self._root


System = SystemManager()

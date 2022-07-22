"""
System manager contains:
* AbstractManager based objects
* Configuration from `$APP/configs/*.json`
"""
from pathlib import Path
from dotty_dict import Dotty

from cloudykit.objects.registry import ManagersRegistry
from cloudykit.utils.logger import DummyLogger
from cloudykit.utils.files import read_json


class SystemManager:
    """ Simple manager that provides access to """
    name = 'system'

    def __init__(self) -> None:
        # Protected/private attrs
        self._root: Path = None
        self._config: Dotty = Dotty({})

        # Public attrs
        self.registry = ManagersRegistry(self)
        self.logger = DummyLogger(self.__class__.__name__)

        super().__init__()

    def mount(self, root: str) -> None:
        self._root = Path(root)

        # Read configs and check if all required configs are in directory
        config = read_json(str(self._root / 'configs/cloudykit.json'))
        req_configs = set(config.get('required_configs', []))
        if req_configs:
            req_diff = set(str(i.name) for i in (self._root / 'configs').iterdir() if i.name != 'cloudykit.json')

            for req in req_configs:
                if req not in req_diff:
                    raise RuntimeError(f'Config section `required_configs` '
                                       f'has difference between existing config files')

    @property
    def root(self):
        return self._root


System = SystemManager()

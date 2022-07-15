from pathlib import Path

from cloudykit.abstracts.manager import IManager
from cloudykit.system.manager import System


class AssetsManager(IManager):
    name = 'assets'

    def __init__(self) -> None:
        self._dictionary = dict()

    def _get_assets(self, root: Path) -> None:
        pass

    def mount(self, parent=None) -> None:
        self._get_assets(parent.root / 'assets')

    def unmount(self, parent=None) -> None:
        pass

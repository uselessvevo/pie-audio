from pathlib import Path

from cloudykit.abstracts.manager import IManager
from cloudykit.system.manager import System


class AssetsManager(IManager):
    name = 'assets'

    def __init__(self) -> None:
        self._dictionary = dict()

    def _get_assets(self, root: Path) -> None:
        """
        Assets folder structure:

        assets \
        ... themes \
        ...... <theme name> \
        ......... fonts - folder with fonts
        ......... icons - folder with icons
        ......... palette.py - PyQt palette settings
        ......... theme.qss - output file from theme.template.qss
        ......... theme.template.qss - theme template file
        ......... variables.json - variables for theme.template.qss
        """
        pass

    def mount(self, parent=None) -> None:
        self._get_assets(parent.root / 'assets')

    def unmount(self, parent=None) -> None:
        pass

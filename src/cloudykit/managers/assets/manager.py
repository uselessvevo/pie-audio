from pathlib import Path

from cloudykit.abstracts.manager import IManager
from cloudykit.system.manager import System


class AssetsManager(IManager):
    name = 'assets'

    def __init__(self) -> None:
        self._dictionary = dict()
        self._theme = System.config.get('user.theme')
        self._assets_folder = System.config.get('assets.assets_folder', 'assets')

    def mount(self, parent=None) -> None:
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
        if not self._theme:
            return

        for file in (parent.root / self._assets_folder / 'themes' / self._theme).iterdir():
            if file.is_dir():
                pass

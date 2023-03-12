from PyQt5.QtWidgets import QShortcut

from piekit.mainwindow.main import MainWindow
from piekit.managers.base import BaseManager
from piekit.managers.structs import SysManagers


class ShortcutsManager(BaseManager):
    """ QShortcuts managers """
    name = SysManagers.Shortcuts

    def __init__(self) -> None:
        super().__init__()

        self._shortcuts: dict[str, QShortcut] = {}

    def mount(self, section: str, shortcut: str, parent: MainWindow = None) -> None:
        pass

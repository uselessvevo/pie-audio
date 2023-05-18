from piekit.mainwindow.main import MainWindow
from piekit.managers.base import BaseManager
from piekit.managers.structs import SysManager

from PySide6.QtGui import QShortcut


class ShortcutsManager(BaseManager):
    """ QShortcuts managers """
    name = SysManager.Shortcuts

    def __init__(self) -> None:
        self._shortcuts: dict[str, QShortcut] = {}

    def init(self, section: str, shortcut: str, parent: MainWindow = None) -> None:
        pass

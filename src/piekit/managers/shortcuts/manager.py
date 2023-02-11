from PyQt5.QtWidgets import QShortcut

from piekit.mainwindow.main import MainWindow
from piekit.managers.base import BaseManager


class ShortcutsManager(BaseManager):
    """ QShortcuts managers """

    def __init__(self) -> None:
        super().__init__()

        self._shortcuts: dict[str, QShortcut] = {}

    def mount(self, shortcut: str, parent: MainWindow = None) -> None:
        pass

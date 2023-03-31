import typing

from PyQt6.QtWidgets import QStatusBar, QWidget

from pieapp.structs.containers import Containers
from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class StatusBar(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = Containers.StatusBar

    def showMessage(self, message: str) -> None:
        self.statusBar.showMessage(message)

    def init(self) -> None:
        self.statusBar = QStatusBar(self._parent)
        self.statusBar.insertPermanentWidget(0, QWidget())
        self._parent.setStatusBar(self.statusBar)


def main(*args, **kwargs) -> typing.Any:
    return StatusBar(*args, **kwargs)

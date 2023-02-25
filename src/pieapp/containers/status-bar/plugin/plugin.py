import typing

from PyQt5.QtWidgets import QStatusBar, QWidget

from piekit.plugins.base import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class StatusBar(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "status-bar"

    def showMessage(self, message: str) -> None:
        self.statusBar.showMessage(message)

    def init(self) -> None:
        self.statusBar = QStatusBar(self._parent)
        self.statusBar.insertPermanentWidget(0, QWidget())
        self._parent.setStatusBar(self.statusBar)


def main(*args, **kwargs) -> typing.Any:
    return StatusBar(*args, **kwargs)

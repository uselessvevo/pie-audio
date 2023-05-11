from __feature__ import snake_case

import typing

from PySide6.QtWidgets import QStatusBar, QWidget

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

    def show_message(self, message: str) -> None:
        self.status_bar.show_message(message)

    def init(self) -> None:
        self.status_bar = QStatusBar(self._parent)
        self.status_bar.insert_permanent_widget(0, QWidget())
        self._parent.set_status_bar(self.status_bar)

    showMessage = show_message


def main(*args, **kwargs) -> typing.Any:
    return StatusBar(*args, **kwargs)
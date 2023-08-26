from __feature__ import snake_case

from typing import Union

from PySide6.QtWidgets import QStatusBar, QWidget

from pieapp.structs.containers import Container
from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin


class StatusBar(
    PiePlugin,
    ConfigAccessorMixin, LocalesAccessorMixin, AssetsAccessorMixin,
):
    name = Container.StatusBar

    def show_message(self, message: str) -> None:
        self.status_bar.show_message(message)

    def init(self) -> None:
        self.status_bar = QStatusBar(self._parent)
        self.status_bar.insert_permanent_widget(0, QWidget())
        self._parent.set_status_bar(self.status_bar)
        self._parent.sig_plugin_ready.connect(lambda _: self.show_message(self.get_translation("Plugins are ready")))

    showMessage = show_message


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    return StatusBar(*args, **kwargs)

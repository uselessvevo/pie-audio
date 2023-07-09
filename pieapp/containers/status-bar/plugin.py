from __feature__ import snake_case

from typing import Union

from PySide6.QtWidgets import QStatusBar, QWidget

from pieapp.structs.containers import Container
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
    name = Container.StatusBar
    version: str = "1.0.0"
    pieapp_version: str = "1.0.0"
    piekit_version: str = "1.0.0"

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

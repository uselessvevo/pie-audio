from PyQt5.QtWidgets import QWidget, QTableWidget

from piekit.plugins.base import BasePlugin

from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.plugins.decorators import on_plugin_available


class ContentTable(
    BasePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "content-table"
    requires = ["workbench"]

    def init(self) -> None:
        self.logger.info("Initializing")
        self.table = QTableWidget()

    @on_plugin_available(plugin="workbench")
    def test(self):
        self.logger.info("##########################Test")
        self._parent.addWidget(self.table)

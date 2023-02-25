import typing

from PyQt5.QtWidgets import QTableWidget

from piekit.plugins.base import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.plugins.decorators import onPluginAvailable


class ContentTable(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "content-table"
    requires = ["workbench"]

    def init(self) -> None:
        self.logger.info("Initializing")
        self.table = QTableWidget()
        # self._parent.addCentralWidget()

    @onPluginAvailable(target="workbench")
    def test(self):
        self.logger.info("##########################Test")


def main(*args, **kwargs) -> typing.Any:
    return ContentTable(*args, **kwargs)

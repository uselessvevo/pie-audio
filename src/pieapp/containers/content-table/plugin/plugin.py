from PyQt5.QtWidgets import QTableWidget

from piekit.containers.containers import PieContainer
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.objects.decorators import onObjectAvailable


class ContentTable(
    PieContainer,
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

    @onObjectAvailable(target="workbench")
    def test(self):
        self.logger.info("##########################Test")

from PySide6.QtWidgets import QTreeWidgetItem

from pieapp.api.plugins.confpage import ConfigPage


class ConfigPageTreeWidgetItem(QTreeWidgetItem):

    def __init__(self, confpage: ConfigPage, index: int) -> None:
        super().__init__()
        self._confpage = confpage
        self._index = index

    @property
    def confpage(self) -> ConfigPage:
        return self._confpage

    @property
    def index(self) -> int:
        return self._index

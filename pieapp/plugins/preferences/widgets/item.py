from PySide6.QtWidgets import QTreeWidgetItem

from pieapp.api.plugins.confpage import ConfigPage


class ConfigPageTreeWidget(QTreeWidgetItem):

    def __init__(self, confpage: ConfigPage) -> None:
        super().__init__()
        self._confpage = confpage

    @property
    def confpage(self) -> ConfigPage:
        return self._confpage

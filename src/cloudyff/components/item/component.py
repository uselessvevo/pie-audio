from PyQt5 import QtWidgets

from cloudykit.abstracts.component import IComponent


class MediaTableItem(IComponent, QtWidgets.QWidget):

    name = 'cloudyff_media_table_item'

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._parent = parent

    def init(self):
        pass

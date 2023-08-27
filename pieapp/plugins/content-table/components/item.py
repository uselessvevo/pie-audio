from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout


class ContentTableItem(QWidget):

    def __init__(self, parent) -> None:
        super(ContentTableItem, self).__init__(parent=parent)

        self._main_vbox_layout = QVBoxLayout()

        self._title_label = QLabel()
        self._title_label.set_object_name('ContentItemTitle')

        self._description_label = QLabel()
        self._description_label.set_object_name('ContentItemDescription')

        self._main_vbox_layout.add_widget(self._title_label)
        self._main_vbox_layout.add_widget(self._description_label)

        self._item_hbox_layout = QHBoxLayout()
        self.set_object_name('ContentItem')
        self._icon = QLabel()

        self._item_hbox_layout.add_widget(self._icon, 0)
        self._item_hbox_layout.add_layout(self._main_vbox_layout, 1)

        self._icon.set_object_name('ContentItem')
        self.set_layout(self._item_hbox_layout)

    def set_title(self, value: str) -> None:
        self._title_label.set_text(value)

    def set_description(self, value: str) -> None:
        self._description_label.set_text(value)

    def set_icon(self, icon: str, width: int = 32, height: int = 32) -> None:
        icon_pixmap = QPixmap(icon)
        icon_pixmap = icon_pixmap.scaled(width, height)
        self._icon.set_pixmap(icon_pixmap)

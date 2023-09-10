from __feature__ import snake_case
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout


class ContentTableItem(QWidget):

    def __init__(self, parent) -> None:
        super(ContentTableItem, self).__init__(parent=parent)

        self._main_vbox_layout = QVBoxLayout()

        self._title_label = QLabel()
        self._title_label.set_object_name("ContentItemTitle")

        self._description_label = QLabel()
        self._description_label.set_object_name("ContentItemDescription")

        self._main_vbox_layout.add_widget(self._title_label)
        self._main_vbox_layout.add_widget(self._description_label)

        self._item_hbox_layout = QHBoxLayout()
        self.set_object_name("ContentItem")
        self._file_format_label = QLabel()

        self._item_hbox_layout.add_widget(self._file_format_label, 0)
        self._item_hbox_layout.add_layout(self._main_vbox_layout, 1)

        self._file_format_label.set_object_name("ContentItem")
        self._file_format_label.set_style_sheet(
            """
            QLabel{
              background-color: #f5a56c;
              font-color: #ffffff;
              border-radius: 10px;
              min-height: 20px;
              min-width: 20px;
            }
            """
        )
        self.set_layout(self._item_hbox_layout)

    def set_title(self, title: str) -> None:
        self._title_label.set_text(title)

    def set_description(self, description: str) -> None:
        self._description_label.set_text(description)

    def set_icon(self, file_format: str) -> None:
        self._file_format_label.set_text(file_format)

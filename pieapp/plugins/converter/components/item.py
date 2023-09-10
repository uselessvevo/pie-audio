from __feature__ import snake_case
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout


class ConverterItemWidget(QWidget):

    def __init__(self, parent) -> None:
        super(ConverterItemWidget, self).__init__(parent=parent)
        self.set_object_name("ConverterItem")

        self._main_vbox_layout = QVBoxLayout()

        self._title_label = QLabel()
        self._title_label.set_object_name("ConverterItemTitle")

        self._description_label = QLabel()
        self._description_label.set_object_name("ConverterItemDescription")

        self._main_vbox_layout.add_widget(self._title_label)
        self._main_vbox_layout.add_widget(self._description_label)

        self._item_hbox_layout = QHBoxLayout()
        self._file_format_label = QLabel()
        self._file_format_label.set_fixed_size(34, 34)
        self._file_format_label.set_object_name("ConverterItemFormat")
        self._file_format_label.set_alignment(Qt.AlignmentFlag.AlignCenter)

        self._item_hbox_layout.add_widget(self._file_format_label, 0)
        self._item_hbox_layout.add_layout(self._main_vbox_layout, 1)
        self.set_layout(self._item_hbox_layout)

    def set_title(self, title: str) -> None:
        self._title_label.set_text(title)

    def set_description(self, description: str) -> None:
        self._description_label.set_text(description)

    def set_icon(self, file_format: str) -> None:
        self._file_format_label.set_text(file_format)

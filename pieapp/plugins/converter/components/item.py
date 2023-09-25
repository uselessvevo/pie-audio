from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QToolButton

from piekit.managers.assets.mixins import AssetsAccessorMixin

from .menu import ConverterItemMenu


class ConverterItemWidget(QWidget, AssetsAccessorMixin):

    def __init__(self, parent, index: int, file_format: str) -> None:
        super(ConverterItemWidget, self).__init__(parent=parent)

        # Index of item
        self._index = index
        self._file_format = file_format

        self.set_object_name("ConverterItem")

        self._main_vbox_layout = QVBoxLayout()

        self._title_label = QLabel()
        self._title_label.set_object_name("ConverterItemTitle")

        self._description_label = QLabel()
        self._description_label.set_object_name("ConverterItemDescription")

        self._item_menu = ConverterItemMenu()
        refresh_toolbutton = QToolButton()
        refresh_toolbutton.set_object_name("ConverterMenuItemTB")
        refresh_toolbutton.set_icon(self.get_svg_icon("refresh.svg"))

        delete_toolbutton = QToolButton()
        delete_toolbutton.set_object_name("ConverterMenuItemTB")
        delete_toolbutton.set_icon(self.get_svg_icon("delete.svg"))

        self._item_menu.add_item("refresh_toolbutton", refresh_toolbutton)
        self._item_menu.add_item("delete_toolbutton", delete_toolbutton)

        self._main_vbox_layout.add_widget(self._item_menu, alignment=Qt.AlignmentFlag.AlignRight)
        self._main_vbox_layout.add_widget(self._title_label)
        self._main_vbox_layout.add_widget(self._description_label)

        self._item_hbox_layout = QHBoxLayout()
        self._file_format_label = QLabel()
        self._file_format_label.set_fixed_size(34, 34)
        self._file_format_label.set_object_name("ConverterItemFormat")
        self._file_format_label.set_alignment(Qt.AlignmentFlag.AlignCenter)
        self._get_file_format_color()

        self._item_hbox_layout.add_widget(self._file_format_label, 0)
        self._item_hbox_layout.add_layout(self._main_vbox_layout, 1)
        self.set_layout(self._item_hbox_layout)

    def _get_file_format_color(self) -> None:
        r, g, b = 245, 165, 105
        self._file_format_label.set_style_sheet(
            "#ConverterItemFormat {background-color: rgb(%s,%s,%s);}" % (r, g, b)
        )

    def set_title(self, title: str) -> None:
        self._title_label.set_text(title)

    def set_description(self, description: str) -> None:
        self._description_label.set_text(description)

    def set_icon(self, file_format: str) -> None:
        self._file_format_label.set_text(file_format)

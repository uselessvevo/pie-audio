from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QToolButton, QStyle

from piekit.managers.assets.mixins import AssetsAccessorMixin


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

        menu_hbox_widget = QWidget()

        pb1 = QToolButton()
        pb1.set_object_name("ConverterMenuItemTB")
        pb1.set_icon(self.get_svg_icon("refresh.svg"))

        pb2 = QToolButton()
        pb2.set_object_name("ConverterMenuItemTB")
        pb2.set_icon(self.get_svg_icon("cancel.svg"))

        menu_hbox = QHBoxLayout()
        menu_hbox.set_contents_margins(1, 1, 1, 1)
        menu_hbox.insert_stretch(-1, 1)
        menu_hbox.add_widget(pb1, alignment=Qt.AlignmentFlag.AlignRight)
        menu_hbox.add_widget(pb2, alignment=Qt.AlignmentFlag.AlignRight)

        menu_hbox_widget.set_layout(menu_hbox)
        menu_hbox_widget.set_object_name("ConverterMenuWidget")

        self._main_vbox_layout.add_widget(menu_hbox_widget, alignment=Qt.AlignmentFlag.AlignRight)
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

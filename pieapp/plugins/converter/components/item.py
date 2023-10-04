from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin

from .menu import ConverterItemMenu


class ConverterItemWidget(QWidget, LocalesAccessorMixin, AssetsAccessorMixin):

    def __init__(self, parent, index: int, file_model: "MediaFile") -> None:
        super(ConverterItemWidget, self).__init__(parent=parent)

        # Index of item
        self._index = index

        self.set_object_name("ConverterItem")

        self._main_vbox_layout = QVBoxLayout()

        self._title_label = QLabel()
        self._title_label.set_object_name("ConverterItemTitle")

        self._description_label = QLabel()
        self._description_label.set_object_name("ConverterItemDescription")

        self._item_menu = ConverterItemMenu()
        self._item_menu.add_item(
            name="delete",
            text=self.get_translation("Delete"),
            icon=self.get_svg_icon("delete.svg"),
            callback=self._delete_toolbutton_connect
        )

        self._main_vbox_layout.add_widget(self._item_menu, alignment=Qt.AlignmentFlag.AlignRight)
        self._main_vbox_layout.add_widget(self._title_label)
        self._main_vbox_layout.add_widget(self._description_label)

        self._item_hbox_layout = QHBoxLayout()
        self._item_hbox_layout.set_contents_margins(12, 10, 10, 10)
        self._file_format_label = QLabel()
        self._file_format_label.set_fixed_size(48, 48)
        self._file_format_label.set_object_name("ConverterItemFormat")
        self._file_format_label.set_alignment(Qt.AlignmentFlag.AlignCenter)
        self._get_file_format_color()

        self._item_hbox_layout.add_widget(self._file_format_label, 0)
        self._item_hbox_layout.add_layout(self._main_vbox_layout, 1)
        self.set_layout(self._item_hbox_layout)

    def _delete_toolbutton_connect(self) -> None:
        pass

    def add_menu_item(self, *args, **kwargs) -> None:
        """
        A proxy method to interact with `ConverterItemMenu`
        """
        self._item_menu.add_item(*args, **kwargs)

    def enter_event(self, event: "QEnterEvent") -> None:
        self._item_menu.show()
        for item in self._item_menu.items:
            item.set_visible(True)

    def leave_event(self, event: "QEvent") -> None:
        self._item_menu.hide()
        for item in self._item_menu.items:
            item.set_visible(False)

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

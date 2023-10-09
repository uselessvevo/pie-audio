from __feature__ import snake_case

from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QToolButton, QListWidgetItem
from pieapp.structs.media import MediaFile

from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin

from .list import ConverterListWidget
from .menu import ConverterItemQuickActions


class ConverterItemWidget(QWidget, LocalesAccessorMixin, AssetsAccessorMixin):

    def __init__(self, parent: ConverterListWidget, media_file: "MediaFile") -> None:
        super(ConverterItemWidget, self).__init__(parent=parent)

        self._parent = parent

        # Index of item
        self._media_file = media_file

        self.set_object_name("ConverterItem")

        self._main_vbox_layout = QVBoxLayout()

        self._title_label = QLabel()
        self._title_label.set_object_name("ConverterItemTitle")

        self._description_label = QLabel()
        self._description_label.set_object_name("ConverterItemDescription")

        self._item_menu = ConverterItemQuickActions(self, media_file)

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

    def set_items_disabled(self) -> None:
        self._item_menu.set_disabled(True)
        for item in self._item_menu.get_items():
            item.set_disabled(True)

    def add_quick_action(
        self,
        name: str,
        text: str,
        icon: QIcon,
        callback: callable = None,
        before: str = None,
        after: str = None,
    ) -> None:
        """
        A proxy method to interact with `ConverterItemMenu`
        """
        self._item_menu.add_item(name, text, icon, callback, before, after)

    def set_list_widget(self, item: QListWidgetItem) -> None:
        self._list_widget = item

    def enter_event(self, event: "QEnterEvent") -> None:
        self._item_menu.show()
        self._parent.set_current_row(self._parent.row(self._list_widget))
        for item in self._item_menu.get_items():
            item.set_visible(True)

    def leave_event(self, event: "QEvent") -> None:
        self._item_menu.hide()
        for item in self._item_menu.get_items():
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

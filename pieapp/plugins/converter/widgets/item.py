from __feature__ import snake_case

from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QListWidgetItem, QGridLayout, QSplitter

from pieapp.helpers.qt import get_main_window
from pieapp.widgets.spacer import Spacer
from pieapp.api.structs.media import MediaFile

from converter.widgets.list import ConverterListWidget
from converter.widgets.menu import QuickActionMenu


class ConverterItem(QWidget):

    def __init__(self, parent: ConverterListWidget, media_file: "MediaFile", color_props: dict = None) -> None:
        super().__init__(parent)

        self._parent = parent
        self._list_widget = None
        self._color_props = color_props or {}

        # Index of item
        self._media_file = media_file

        self.set_object_name("ConverterItem")

        self._title_label = QLabel()
        self._title_label.set_object_name("ConverterItemTitle")

        self._description_label = QLabel()
        self._description_label.set_object_name("ConverterItemDescription")

        self._quick_action_menu = QuickActionMenu(media_file=media_file)

        main_grid_layout = QGridLayout()

        title_vbox = QVBoxLayout()
        title_vbox.add_widget(self._title_label, alignment=Qt.AlignmentFlag.AlignLeft)
        title_vbox.add_widget(self._description_label, alignment=Qt.AlignmentFlag.AlignLeft)

        quick_action_hbox = QHBoxLayout()
        quick_action_hbox.add_widget(self._quick_action_menu, alignment=Qt.AlignmentFlag.AlignRight)

        main_grid_layout.add_layout(title_vbox, 0, 0, Qt.AlignmentFlag.AlignLeft)
        main_grid_layout.add_layout(quick_action_hbox, 0, 1, Qt.AlignmentFlag.AlignRight)
        main_grid_layout.add_widget(QSplitter(Qt.Orientation.Horizontal), 1, 1, Qt.AlignmentFlag.AlignBottom)

        item_hbox_layout = QHBoxLayout()
        item_hbox_layout.set_contents_margins(12, 15, 10, 15)

        self._file_format_label = QLabel()
        self._file_format_label.set_fixed_size(48, 48)
        self._file_format_label.set_object_name("ConverterItemFormat")
        self._file_format_label.set_alignment(Qt.AlignmentFlag.AlignCenter)
        self._get_file_format_color()

        item_hbox_layout.add_widget(self._file_format_label, 0)
        item_hbox_layout.add_layout(main_grid_layout, 1)
        self.set_layout(item_hbox_layout)

    @property
    def media_file(self) -> MediaFile:
        return self._media_file

    def set_items_disabled(self) -> None:
        self._quick_action_menu.set_disabled(True)
        for item in self._quick_action_menu.get_items():
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
        self._quick_action_menu.add_item(name, text, icon, callback, before, after)

    def set_list_widget(self, item: QListWidgetItem) -> None:
        self._list_widget = item

    def enter_event(self, event: "QEnterEvent") -> None:
        self._quick_action_menu.show()
        self._parent.set_current_row(self._parent.row(self._list_widget))
        for item in self._quick_action_menu.get_items():
            item.set_visible(True)

    def leave_event(self, event: "QEvent") -> None:
        self._quick_action_menu.hide()
        for item in self._quick_action_menu.get_items():
            item.set_visible(False)

    def set_title(self, title: str) -> None:
        self._title_label.set_text(f"{title[0:60]}...")
        self._title_label.set_tool_tip(title)

    def set_description(self, description: str) -> None:
        self._description_label.set_text(description)

    def set_icon(self, file_format: str) -> None:
        self._file_format_label.set_text(file_format)

    def _get_file_format_color(self) -> None:
        color = self._color_props.get(self._media_file.info.file_format, self._color_props.get("default"))
        self._file_format_label.set_style_sheet(
            "#ConverterItemFormat {background-color: %s;}" % color
        )

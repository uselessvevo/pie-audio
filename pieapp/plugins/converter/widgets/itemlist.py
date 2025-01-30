from __feature__ import snake_case

from PySide6.QtGui import Qt, QIcon
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QSplitter
from PySide6.QtWidgets import QToolButton
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QListWidgetItem

from pieapp.widgets.buttons import Button
from pieapp.widgets.buttons import ButtonRole
from pieapp.api.converter.models import MediaFile
from pieapp.api.registries.snapshots.registry import SnapshotRegistry

from converter.widgets.contentlist import ContentListWidget
from converter.widgets.itemmenu import QuickActionMenu


class QuickActionList(QWidget):
    """
    This widget contains all buttons and is stored (rendered) on the QListWidgetItem.
    """
    sig_snapshot_modified = Signal(MediaFile)

    def __init__(
        self,
        parent: ContentListWidget,
        media_file_name: str
    ) -> None:
        super().__init__(parent)

        self._parent = parent
        self._list_widget = None
        self._media_file_name = media_file_name

        self.set_object_name("ConverterItem")

        self._title_label = QLabel()
        self._title_label.set_size_policy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self._title_label.set_object_name("ConverterItemTitle")

        self._description_label = QLabel()
        self._description_label.set_object_name("ConverterItemDescription")
        self._quick_action_menu = QuickActionMenu(self, media_file_name)

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

        self._action_button = Button(ButtonRole.Default)
        self._action_button.set_fixed_size(48, 48)
        self._action_button.set_object_name("ConverterItemFormat")
        # self._file_format_label.set_alignment(Qt.AlignmentFlag.AlignCenter)
        self._get_file_format_color()

        item_hbox_layout.add_widget(self._action_button, 0)
        item_hbox_layout.add_layout(main_grid_layout, 1)
        self.set_layout(item_hbox_layout)

        self.sig_snapshot_modified.connect(self.on_snapshot_modified)

    @Slot(MediaFile)
    def on_snapshot_modified(self, media_file: MediaFile) -> None:
        media_file = SnapshotRegistry.get(media_file.name)
        if self._media_file_name != media_file.name:
            return

        media_file = SnapshotRegistry.get(media_file.name)
        if not media_file:
            return

        self.set_title(media_file.info.filename)
        # TODO: Добавить список с ед. измерений в настройках конвертора
        self.set_description(f"{media_file.info.bit_rate}kb/s")
        # self.set_icon()

    @property
    def media_file_name(self) -> str:
        return self._media_file_name

    def set_items_disabled(self) -> None:
        self._quick_action_menu.set_enabled(False)
        for item in self._quick_action_menu.get_items():
            item.set_enabled(False)

    def add_quick_action(
        self,
        name: str,
        text: str,
        icon: QIcon,
        callback: callable = None,
        before: str = None,
        after: str = None,
        enabled: bool = False,
    ) -> QToolButton:
        """
        A proxy method to interact with `ConverterItemMenu`
        """
        return self._quick_action_menu.add_item(
            name=name,
            text=text,
            icon=icon,
            callback=callback,
            before=before,
            after=after,
            enabled=enabled
        )

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
        if len(title) >= 50:
            title = f"{title[:50]}..."
        self._title_label.set_text(title)
        self._title_label.set_tool_tip(title)

    def set_description(self, description: str) -> None:
        self._description_label.set_text(description)

    def set_icon(self, icon: QIcon) -> None:
        self._action_button.set_icon(icon)

    def _get_file_format_color(self) -> None:
        media_file = SnapshotRegistry.get(self._media_file_name)
        # self._file_format_label.set_style_sheet("#ConverterItemFormat {background-color: %s;}" % color)

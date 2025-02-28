from __feature__ import snake_case

import os

from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
from PySide6.QtCore import Signal

from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QSizePolicy

from pieapp.api.globals import Global
from pieapp.api.utils.qt import get_main_window
from pieapp.api.utils.logger import logger

from pieapp.api.models.scopes import Scope
from pieapp.api.models.themes import IconName
from pieapp.api.models.themes import ThemeProperties
from pieapp.api.models.toolbars import ToolBarItem
from pieapp.api.converter.models import MediaFile

from pieapp.api.plugins.widgets import PiePluginWidget
from pieapp.api.plugins.mixins import CoreAccessorsMixin
from pieapp.api.plugins.mixins import WidgetsAccessorMixins

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.snapshots.registry import SnapshotRegistry
from pieapp.api.registries.quickactions.registry import QuickActionRegistry

from converter.widgets.quickaction import DeleteQuickAction
from pieapp.widgets.waitingspinner import create_wait_spinner

from converter.widgets.itemlist import QuickActionList
from converter.widgets.search import ContentListSearch
from converter.widgets.contentlist import ContentListWidget


class ConverterWidget(PiePluginWidget, CoreAccessorsMixin, WidgetsAccessorMixins):
    # Emit on files selected in open file dialog
    sig_files_selected = Signal(list)

    # Emit on snapshot created
    sig_snapshot_created = Signal(MediaFile)

    # Emit on snapshot deleted
    sig_snapshot_deleted = Signal(MediaFile)

    # Emit on snapshot modified
    sig_snapshot_modified = Signal(MediaFile)

    # Emit on global snapshot restored
    sig_snapshots_restored = Signal()

    # Emit on new list item added
    sig_table_item_added = Signal(MediaFile)

    def init(self) -> None:
        self.supported_formats = ""
        for audio_extension in Global.AUDIO_EXTENSIONS:
            description, file_format = audio_extension
            self.supported_formats += f"{translate(description)} {file_format} ;; "

        # Prepare widget
        self._converter_item_widgets: list[QuickActionList] = []
        self._main_grid_layout = QGridLayout()
        self._main_grid_layout.set_spacing(0)
        self._main_grid_layout.set_contents_margins(0, 0, 0, 0)

        # Setup content list
        self._content_list_widget = ContentListWidget()
        self._content_list_widget.sig_item_pressed.connect(self.content_list_item_selected)
        self._content_list_widget.sig_item_changed.connect(self.content_list_item_removed)
        self._content_list_widget.sig_item_deleted.connect(self.content_list_item_removed)

        # Setup search field
        self._search = ContentListSearch()
        self._search.set_minimum_size(32, 32)
        self._search.set_placeholder_text(translate("Search"))
        self._search.set_hidden(True)
        self._search.textChanged.connect(self.on_search_text_changed)

        self._spinner = create_wait_spinner(
            self._content_list_widget,
            size=64,
            number_of_lines=30,
            inner_radius=10,
            color=self.get_theme_property(ThemeProperties.MainFontColor)
        )

        self._pixmap_label = QLabel()
        self._pixmap_label.set_pixmap(self.get_icon(IconName.MusicNote).pixmap(100))
        self._pixmap_label.set_alignment(Qt.AlignmentFlag.AlignCenter)

        self._text_label = QLabel()
        self._text_label.set_text(translate("No files selected"))
        self._text_label.set_alignment(Qt.AlignmentFlag.AlignCenter)

        main_window = get_main_window()
        self._spacer_widget = QSpacerItem(
            main_window.width() // 2,
            main_window.height() // 2,
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Maximum
        )

        self._placeholder_layout = QVBoxLayout()
        self._placeholder_layout.add_item(self._spacer_widget)
        self._placeholder_layout.add_widget(self._pixmap_label)
        self._placeholder_layout.add_widget(self._text_label)
        self._placeholder_layout.add_item(self._spacer_widget)

        self._placeholder_widget = QWidget()
        self._placeholder_widget.set_layout(self._placeholder_layout)

        self._main_grid_layout.add_widget(self._placeholder_widget, 0, 0, Qt.AlignmentFlag.AlignCenter)

    def get_main_layout(self) -> "QLayout":
        return self._main_grid_layout

    @property
    def content_list_widget(self) -> ContentListWidget:
        return self._content_list_widget

    def connect_snapshot_signals(self) -> None:
        self.sig_snapshot_created.connect(SnapshotRegistry.sig_snapshot_created)
        self.sig_snapshot_deleted.connect(SnapshotRegistry.sig_snapshot_deleted)
        self.sig_snapshot_modified.connect(SnapshotRegistry.sig_snapshot_modified)
        self.sig_snapshots_restored.connect(SnapshotRegistry.sig_snapshots_restored)

    # Search bar methods

    def toggle_search(self) -> None:
        self._search.set_hidden(not self._search.is_hidden())
        self._search.set_focus()

    @Slot(str)
    def on_search_text_changed(self, text: str) -> None:
        """
        Filter `content_list` by text
        """
        for row in range(self._content_list_widget.count()):
            item = self._content_list_widget.item(row)
            item_widget = self._content_list_widget.item_widget(item)
            if text:
                item.set_hidden(not (text.lower() in item_widget.media_file.info.filename.lower()))
            else:
                item.set_hidden(False)

    # Placeholder methods

    def _set_placeholder(self) -> None:
        """
        Show placeholder
        """
        if not self._placeholder_layout.find_child(self._pixmap_label.__class__, self._pixmap_label.object_name()):
            self._placeholder_layout.add_widget(self._pixmap_label)
            self._placeholder_layout.add_widget(self._text_label)

    def _clear_placeholder(self) -> None:
        """
        Remove placeholder
        """
        self._placeholder_widget.set_visible(False)
        # self._placeholder_layout.remove_widget(self._text_label)
        # self._placeholder_layout.remove_widget(self._pixmap_label)
        # self._main_grid_layout.remove_item(self._placeholder_layout)

    # File system methods

    def open_files(self) -> None:
        last_opened_directory = self.get_app_config(
            "workflow.last_opened_directory",
            Scope.User,
            os.path.expanduser("~")
        )
        last_opened_directory = str(last_opened_directory)
        selected_files = QFileDialog.get_open_file_names(
            caption=translate("Open files"),
            dir=last_opened_directory,
            filter=self.supported_formats
        )
        selected_files = selected_files[0]
        if not selected_files:
            return

        self.sig_files_selected.emit(selected_files)

    # ContentList methods

    def content_list_item_removed(self) -> None:
        """
        Disable `clear` button on empty `content_list`
        """
        if self._content_list_widget.count() == 0:
            self.get_tool_button(self.name, ToolBarItem.Clear).set_enabled(False)

    def content_list_item_selected(self, *args, **kwargs) -> None:
        # TODO:
        # 1. Change GlobalContext
        # 2. Trigger toolbar items context and show what toolbar items we can use
        logger.debug(f"{args}, {kwargs}")

    def clear_content_list(self) -> None:
        """
        Clear content list, remove it from the `list_grid_layout` and disable clear button
        """
        self._converter_item_widgets = []
        self._content_list_widget.clear()
        self._set_placeholder()
        self.get_tool_button(self.name, ToolBarItem.Clear).set_enabled(False)

    # Plugin to Widget methods - ProbeWorker

    def probe_worker_started(self) -> None:
        self._clear_placeholder()
        self._main_grid_layout.add_widget(self._spinner, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._spinner.start()

    def probe_worker_finished(self) -> None:
        self._spinner.stop()
        if not self._main_grid_layout.find_child(self._spinner.__class__, self._spinner.object_name()):
            self._spinner.set_visible(False)

    def probe_worker_failed(self) -> None:
        self._spinner.stop()

    # Plugin to Widget methods - CopyFilesWorker

    def copy_files_worker_failed(self) -> None:
        self._spinner.stop()

    # File System events methods

    def on_file_created(self, index: int, media_file: MediaFile) -> None:
        """
        Update QuickAction and show that progress is unsaved
        """
        pass

    def on_file_moved(self, index: int, media_file: MediaFile) -> None:
        """
        Skip files in snapshot's temp folders. Display warning message when ORIGINAL file was moved
        """
        pass

    def on_file_deleted(self, index) -> None:
        self._content_list_widget.take_item(index)
        del self._converter_item_widgets[index]
        if len(self._converter_item_widgets) < 1:
            self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(True)

    # Plugin to Widget methods - SnapshotRegistry signals handlers

    def on_snapshot_created(self):
        self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(True)

    def on_snapshot_deleted(self, index: int, media_file: MediaFile):
        self._content_list_widget.take_item(index)
        del self._converter_item_widgets[index]
        if len(self._converter_item_widgets) < 1:
            self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(True)

    def on_snapshot_modified(self, state: bool, media_file: MediaFile):
        self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(state)

    def on_snapshots_restored(self):
        self.clear_content_list()
        self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(False)

    # QuickAction methods

    def render_quick_actions(self, media_files: list):
        if not media_files:
            return

        self._clear_placeholder()
        self._main_grid_layout.add_widget(self._search, 0, 0)
        self._main_grid_layout.add_widget(self._content_list_widget, 1, 0)

        for media_file in media_files:
            # TODO: Добавить встроенный элемент с краткой информацией по файлу
            # TODO: Добавить меню со второстепенными/неважными элементами, чтобы не переполнять меню
            quick_action_list = QuickActionList(self._content_list_widget, media_file.name)
            quick_action_list.set_title(media_file.info.filename)
            quick_action_list.set_description(media_file.info.bit_rate_string)
            quick_action_list.sig_snapshot_modified.connect(self.sig_snapshot_modified)

            # Render registered QuickActions
            for quick_action in QuickActionRegistry.values():
                quick_action.set_snapshot_name(media_file.name)
                quick_action_list.add_quick_action(quick_action)

            # Render default QuickActions
            delete_quick_action = DeleteQuickAction(self.plugin, enabled=True)
            delete_quick_action.set_snapshot_name(media_file.name)
            quick_action_list.add_quick_action(delete_quick_action)

            widget_layout = QHBoxLayout()
            widget_layout.add_stretch()
            widget_layout.add_widget(quick_action_list)

            item = QListWidgetItem()
            item.set_size_hint(quick_action_list.size_hint())

            # A really nasty hack to get item `row` inside `QWidgetItem`
            quick_action_list.set_list_widget(item)

            self._content_list_widget.add_item(item)
            self._content_list_widget.set_item_widget(item, quick_action_list)
            self._converter_item_widgets.append(quick_action_list)
            self.sig_table_item_added.emit(media_file)

        self.get_tool_button(self.name, ToolBarItem.Clear).set_enabled(True)

import copy
import random
import uuid
from typing import Union
from pathlib import Path

from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QGridLayout, QToolButton
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel, QFileDialog
from PySide6.QtWidgets import QListWidgetItem

from pieapp.api.models.themes import ThemeProperties
from pieapp.api.registries.registry import Registry
from pieapp.helpers.files import delete_files

from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_ready
from pieapp.api.plugins.decorators import on_plugin_shutdown
from pieapp.api.plugins.mixins import CoreAccessorsMixin
from pieapp.api.plugins.mixins import LayoutAccessorsMixins

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.models import Scope, SysRegistry
from pieapp.api.models.layouts import Layout
from pieapp.api.models.media import MediaFile
from pieapp.api.models.menus import MainMenu
from pieapp.api.models.menus import MainMenuItem
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.workbench import WorkbenchItem
from converter.services.observers import FileSystemWatcher

from pieapp.api.models.indexes import Index
from pieapp.helpers.logger import logger
from pieapp.widgets.waitingspinner import create_wait_spinner

from converter.models import ConverterThemeProperties
from converter.confpage import ConverterConfigPage
from converter.widgets.item import ConverterItem
from converter.widgets.list import ConverterListWidget
from converter.widgets.search import ConverterSearch
from converter.services.workers import ConverterProbeWorker, CopyFilesWorker


class Converter(PiePlugin, CoreAccessorsMixin, LayoutAccessorsMixins):
    name = SysPlugin.Converter
    requires = [SysPlugin.MainToolBar, SysPlugin.Preferences, SysPlugin.Layout, SysPlugin.Shortcut]
    optional = [SysPlugin.MainMenuBar, SysPlugin.StatusBar]

    # Emit when converter table item was added
    sig_table_item_added = Signal()

    # Emit when converter table is ready
    sig_converter_table_ready = Signal()

    # Emit on file created
    sig_on_file_created = Signal(str, bool)

    # Emit on file moved
    sig_on_file_moved = Signal(str, str, bool)

    # Emit on file deleted
    sig_on_file_deleted = Signal(str, bool)

    # Emit on file modified
    sig_on_file_modified = Signal(str, bool)

    # Emit on snapshot created
    sig_on_snapshot_created = Signal(MediaFile)

    # Emit on snapshot deleted
    sig_on_snapshot_deleted = Signal(MediaFile)

    # Emit on snapshot modified
    sig_on_snapshot_modified = Signal(MediaFile)

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg")

    @staticmethod
    def get_config_page() -> ConverterConfigPage:
        return ConverterConfigPage()

    def init(self) -> None:
        self._snapshots = Registry(SysRegistry.Snapshots)
        self._temp_directory = Path(self.get_config("workflow.temp_directory", Scope.User))

        self._watcher = FileSystemWatcher(self)
        self._watcher.connect_signals(self)

        self._chunk_size = self.get_config("ffmpeg.chunk_size", Scope.User, 10)
        self._ffmpeg_command = Path(self.get_config("ffmpeg.ffmpeg", Scope.User, "ffmpeg"))
        self._ffprobe_command = Path(self.get_config("ffmpeg.ffprobe", Scope.User, "ffprobe"))

        self._converter_item_widgets: list[ConverterItem] = []
        self._quick_action_items: list[dict[str, QToolButton]] = []

        # Setup grid layouts
        self._list_grid_layout = QGridLayout()

        # Setup content list
        self._content_list = ConverterListWidget(
            change_callback=self._content_list_item_removed,
            remove_callback=self._content_list_item_removed
        )

        # Setup search field
        self._search = ConverterSearch()
        self._search.set_hidden(True)
        self._search.textChanged.connect(self._on_search_text_changed)

        self._spinner = create_wait_spinner(
            self._content_list,
            size=64,
            number_of_lines=30,
            inner_radius=10,
            color=self.get_theme_property(ThemeProperties.MainFontColor)
        )

        self._pixmap_label = QLabel()
        self._pixmap_label.set_pixmap(self.get_icon("icons/package.svg", scope=self.name).pixmap(100))
        self._pixmap_label.set_alignment(Qt.AlignmentFlag.AlignCenter)

        self._text_label = QLabel()
        self._text_label.set_text(translate("No files selected"))
        self._text_label.set_alignment(Qt.AlignmentFlag.AlignCenter)

        # Setup placeholder
        self._set_placeholder()

    # QuickAction public proxy methods

    def disable_side_menu_items(self) -> None:
        """
        A proxy method to disable all QuickActionMenu's items
        """
        for item in self._converter_item_widgets:
            item.set_items_disabled()

    def get_quick_action(self, index: int, name: str = None) -> Union[QToolButton, None]:
        try:
            return self._quick_action_items[index][name]
        except IndexError:
            return

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
        A proxy method to add an item in the QuickActionMenu
        """
        for index, item in enumerate(self._converter_item_widgets):
            tool_button = item.add_quick_action(name, text, icon, callback, before, after)
            self._quick_action_items.insert(index, {name: tool_button})

    # Private widget methods

    def _fill_content_list(self, media_files: list[MediaFile]) -> None:
        if not media_files:
            return

        self._clear_placeholder()
        self._list_grid_layout.add_widget(self._search, 0, 0)
        self._list_grid_layout.add_widget(self._content_list, 1, 0)

        for index, media_file in enumerate(media_files):
            # TODO: Добавить встроенный элемент с краткой информацией по файлу
            # TODO: Добавить меню со второстепенными/неважными элементами, чтобы не переполнять меню
            widget = ConverterItem(
                parent=self._content_list,
                media_file=media_file,
                sig_on_file_modified=self.sig_on_file_modified,
                color_props=self.get_theme_property(ConverterThemeProperties.ConverterItemColors)
            )

            # Add default buttons
            widget.add_quick_action(
                name="delete",
                text=translate("Delete"),
                icon=self.get_svg_icon("icons/delete.svg", self.get_theme_property(ThemeProperties.ErrorColor)),
                callback=self._delete_tool_button_connect
            )
            widget.add_quick_action(
                name="debug.spawn_media_file_copy",
                text=translate("[DEBUG] Spawn media file copy"),
                icon=self.get_svg_icon("icons/help.svg", self.get_theme_property(ThemeProperties.DangerColor)),
                callback=self._debug_spawn_media_file_copy
            )

            widget_layout = QHBoxLayout()
            widget_layout.add_stretch()
            widget_layout.add_widget(widget)

            item = QListWidgetItem()
            item.set_size_hint(widget.size_hint())

            # A really nasty hack to get item `row` inside `QWidgetItem`
            widget.set_list_widget(item)

            self._content_list.add_item(item)
            self._content_list.set_item_widget(item, widget)

            self._converter_item_widgets.append(widget)
            self.sig_table_item_added.emit()

        self.get_tool_button(self.name, WorkbenchItem.Clear).set_disabled(False)
        self.sig_converter_table_ready.emit()

    # ConverterListWidget private methods

    def _content_list_item_removed(self) -> None:
        """
        Disable `clear` button on empty `content_list`
        """
        if self._content_list.count() == 0:
            self.get_tool_button(self.name, WorkbenchItem.Clear).set_disabled(True)

    def _set_placeholder(self) -> None:
        """
        Show placeholder
        """
        if not self._list_grid_layout.find_child(self._pixmap_label.__class__, self._pixmap_label.object_name()):
            self._list_grid_layout.add_widget(self._pixmap_label, 0, 0, alignment=Qt.AlignmentFlag.AlignVCenter)

        if not self._list_grid_layout.find_child(self._text_label.__class__, self._text_label.object_name()):
            self._list_grid_layout.add_widget(self._text_label, 1, 0, alignment=Qt.AlignmentFlag.AlignVCenter)

    def _clear_placeholder(self) -> None:
        """
        Remove placeholder
        """
        self._text_label.set_visible(False)
        self._pixmap_label.set_visible(False)

    def _clear_content_list(self) -> None:
        """
        Clear content list, remove it from the `list_grid_layout` and disable clear button
        """
        self._converter_item_widgets = []
        self._content_list.clear()

        self._list_grid_layout.remove_widget(self._search)
        self._list_grid_layout.remove_widget(self._content_list)
        self._set_placeholder()

        delete_files(self._snapshots.values(as_path=True)[0])
        self._snapshots.restore()
        self.get_tool_button(self.name, WorkbenchItem.Clear).set_disabled(True)

    def _delete_tool_button_connect(self, media_file_name: str) -> None:
        media_file: MediaFile = self._snapshots.get(media_file_name)
        delete_files([media_file.path])

    # ConverterSearch private methods

    def _toggle_search(self) -> None:
        self._search.set_hidden(not self._search.is_hidden())
        self._search.set_focus()

    @Slot(str)
    def _on_search_text_changed(self, text: str) -> None:
        """
        Filter `content_list` by text
        """
        for row in range(self._content_list.count()):
            item = self._content_list.item(row)
            item_widget = self._content_list.item_widget(item)
            if text:
                item.set_hidden(not (text.lower() in item_widget.media_file.info.filename.lower()))
            else:
                item.set_hidden(False)

    # Public API methods

    def open_files(self) -> None:
        selected_files = QFileDialog.get_open_file_names(caption=translate("Open files"))[0]
        if not selected_files:
            return

        selected_files = list(map(Path, selected_files))

        copy_files_worker = CopyFilesWorker(selected_files, self._temp_directory)
        copy_files_worker.signals.failed.connect(self._copy_files_worker_failed)
        copy_files_worker.signals.completed.connect(lambda: self._start_converter_worker(selected_files))
        copy_files_worker.signals.destroyed.connect(self.destroyed)

        pool = QThreadPool.global_instance()
        pool.start(copy_files_worker)

    def _start_converter_worker(self, selected_files: list[Path]) -> None:
        selected_media_files = []
        for selected_file in selected_files:
            media_file = MediaFile(
                uuid=str(uuid.uuid4()),
                name=f"{selected_file.parts[-2]}/{selected_file.name}",
                path=Path(selected_file)
            )
            selected_media_files.append(media_file)

        for index, media_file in enumerate(selected_media_files):
            if media_file.name not in self._snapshots:
                self._snapshots.add(media_file)
            else:
                del selected_media_files[index]

        converter_worker = ConverterProbeWorker(
            media_files=selected_media_files,
            temp_folder=self._temp_directory,
            ffmpeg_cmd=self._ffmpeg_command,
            ffprobe_cmd=self._ffprobe_command,
        )
        converter_worker.signals.started.connect(self._converter_worker_started)
        converter_worker.signals.completed.connect(self._converter_worker_finished)
        converter_worker.signals.failed.connect(self._converter_worker_failed)
        converter_worker.signals.destroyed.connect(self.destroyed)

        pool = QThreadPool.global_instance()
        pool.start(converter_worker)

    # Private background workers and observer methods

    @Slot(Path, bool)
    def on_file_created(self, file_path: Path, is_directory: bool) -> None:
        # TODO: Display notification that new file was added if `media_file` is directory
        #       Then process new files via ConverterProbeWorker
        # self._snapshots.sig_on_file_created.emit(media_file, is_directory)
        # self._start_converter_worker([file_path])
        self.sig_on_file_created.emit(file_path, is_directory)

    @Slot(Path, str, bool)
    def on_file_moved(self, file_path: Path, new_media_file: str, is_directory: bool) -> None:
        media_file = self._snapshots.get(f"{file_path.parts[-2]}/{file_path.name}")
        self._snapshots.update(media_file.name, new_media_file)
        # self.sig_on_snapshot_modified.emit(media_file, new_media_file, is_directory)
        self.sig_on_file_moved.emit(media_file, new_media_file, is_directory)

    @Slot(Path, bool)
    def on_file_deleted(self, file_path: Path, is_directory: bool) -> None:
        if not file_path.exists():
            return
        media_file = self._snapshots.get(f"{file_path.parts[-2]}/{file_path.name}")
        index = self._snapshots.index(media_file.name)
        self._snapshots.remove(media_file.name)
        self._content_list.take_item(index)
        # self._snapshots.sig_on_file_deleted.emit(media_file, is_directory)
        self.sig_on_file_deleted.emit(media_file, is_directory)

    @Slot(Path, bool)
    def on_file_modified(self, file_path: Path, is_directory: bool) -> None:
        # TODO: Process modified file via ConverterProbeWorker
        media_file = self._snapshots.get(f"{file_path.parts[-2]}/{file_path.name}")
        self._snapshots.update(media_file.name, media_file, Index.End)
        self.sig_on_file_modified.emit(media_file, is_directory)

    @Slot(Exception)
    def _copy_files_worker_failed(self, exception: Exception):
        self._spinner.stop()
        status_bar = get_plugin(SysPlugin.StatusBar)
        if status_bar:
            status_bar.show_message(translate("Failed to load files: %s" % str(exception)))

    def _converter_worker_started(self) -> None:
        self._clear_placeholder()
        self._list_grid_layout.add_widget(self._spinner, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._spinner.start()

    @Slot(Path)
    def _converter_worker_finished(self, models_list: list[MediaFile]) -> None:
        self._watcher.start(str(self._temp_directory))
        self._spinner.stop()

        if not self._list_grid_layout.find_child(self._spinner.__class__, self._spinner.object_name()):
            self._spinner.set_visible(False)

        self._fill_content_list(models_list)

        status_bar = get_plugin(SysPlugin.StatusBar)
        if status_bar:
            status_bar.show_message(translate(f"Loaded %s files", len(models_list)))

    @Slot(Exception)
    def _converter_worker_failed(self, exception: Exception) -> None:
        self._spinner.stop()
        status_bar = get_plugin(SysPlugin.StatusBar)
        if status_bar:
            status_bar.show_message(translate("Failed to load files: %s" % str(exception)))

    # Debug methods

    def _debug_print_snapshots(self) -> None:
        for global_snapshot in self._snapshots._global_snapshots:
            logger.debug(global_snapshot)
        # for media_file in self._snapshots.values():
        #     logger.debug(media_file)

    def _debug_spawn_media_file_copy(self, media_file_name: str) -> None:
        snapshot = copy.copy(self._snapshots.get(media_file_name))
        snapshot.uuid = str(uuid.uuid4())
        snapshot.info.file_format = random.choice(["flac", "wav", "test", "ass"])
        self._snapshots.update(snapshot.name, snapshot)
        self._snapshots.add_global_snapshot(snapshot)

    # Shortcut methods

    def _undo_button_connect(self) -> MediaFile:
        snapshot = self._snapshots.set_global_snapshot_index(-1)
        self.sig_on_snapshot_modified.emit(snapshot)
        return snapshot

    def _redo_button_connect(self) -> MediaFile:
        snapshot = self._snapshots.set_global_snapshot_index(+1)
        self.sig_on_snapshot_modified.emit(snapshot)
        return snapshot

    # Plugin event method

    @on_plugin_ready(plugin=SysPlugin.Layout)
    def _on_layout_manager_available(self) -> None:
        layout_manager = get_plugin(SysPlugin.Layout)
        main_layout = layout_manager.get_layout(Layout.Main)
        if main_layout:
            main_layout.add_layout(self._list_grid_layout, 1, 0, Qt.AlignmentFlag.AlignTop)
            layout_manager.add_layout(self.name, main_layout)

    @on_plugin_ready(plugin=SysPlugin.Shortcut)
    def _on_shortcut_manager_ready(self) -> None:
        shortcut = get_plugin(SysPlugin.Shortcut)
        shortcut.add_shortcut(
            name="open_files",
            shortcut="Ctrl+O",
            triggered=self.open_files,
            target=self.parent(),
            title=translate("Open files"),
            description=translate("Open files to process them")
        )
        shortcut.add_shortcut(
            name="toggle_search",
            shortcut="Ctrl+F",
            triggered=self._toggle_search,
            target=self._content_list,
            title=translate("Toggle search input"),
            description=translate("Toggle search input in converter content list")
        )
        shortcut.add_shortcut(
            name="debug.print_snapshots",
            shortcut="Ctrl+D",
            target=self._content_list,
            triggered=self._debug_print_snapshots,
            title=translate("Print snapshots"),
            description=translate("Print snapshots"),
            hidden=True
        )
        shortcut.add_shortcut(
            name="media_file.undo",
            shortcut="Ctrl+Z",
            target=self._content_list,
            triggered=self._undo_button_connect,
            title=translate("Undo"),
            description=translate("Undo file state"),
            hidden=True
        )
        shortcut.add_shortcut(
            name="media_file.redo",
            shortcut="Ctrl+Y",
            target=self._content_list,
            triggered=self._redo_button_connect,
            title=translate("Redo"),
            description=translate("Redo file state"),
            hidden=True
        )

    @on_plugin_ready(plugin=SysPlugin.Preferences)
    def _on_preferences_available(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.register_config_page(self)

    @on_plugin_shutdown(plugin=SysPlugin.Preferences)
    def _on_preferences_teardown(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.deregister_config_page(self)

    @on_plugin_ready(plugin=SysPlugin.MainMenuBar)
    def _on_menu_bar_available(self) -> None:
        """
        Add open file element in the "File" menu
        """
        plugin = get_plugin(SysPlugin.MainMenuBar)
        plugin.add_menu_item(
            scope=Scope.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.OpenFiles,
            text=translate("Open file"),
            icon=self.get_svg_icon("icons/folder-open.svg"),
            index=Index.Start,
            triggered=self.open_files
        )

    @on_plugin_ready(plugin=SysPlugin.MainToolBar)
    def _on_toolbar_available(self) -> None:
        """
        Add tool button on the `Workbench`
        """
        self.add_tool_button(
            scope=self.name,
            name=WorkbenchItem.OpenFiles,
            text=translate("Open file"),
            tooltip=translate("Open file"),
            icon=self.get_svg_icon("icons/folder.svg"),
            triggered=self.open_files
        )

        self.add_tool_button(
            scope=self.name,
            name=WorkbenchItem.Convert,
            text=translate("Convert"),
            tooltip=translate("Convert"),
            icon=self.get_svg_icon("icons/bolt.svg")
        ).set_enabled(False)

        clear_tool_button = self.add_tool_button(
            scope=self.name,
            name=WorkbenchItem.Clear,
            text=translate("Clear"),
            tooltip=translate("Clear"),
            icon=self.get_svg_icon("icons/delete.svg")
        )
        clear_tool_button.set_enabled(False)
        clear_tool_button.clicked.connect(self._clear_content_list)

        self.add_toolbar_item(
            toolbar=SysPlugin.MainToolBar,
            name=WorkbenchItem.OpenFiles,
            item=self.get_tool_button(self.name, WorkbenchItem.OpenFiles),
        )

        self.add_toolbar_item(
            toolbar=SysPlugin.MainToolBar,
            name=WorkbenchItem.Convert,
            item=self.get_tool_button(self.name, WorkbenchItem.Convert),
            after=WorkbenchItem.OpenFiles
        )

        self.add_toolbar_item(
            toolbar=SysPlugin.MainToolBar,
            name=WorkbenchItem.Clear,
            item=self.get_tool_button(self.name, WorkbenchItem.Clear),
            after=WorkbenchItem.Convert
        )


def main(parent: "QMainWindow", plugin_path: "Path"):
    return Converter(parent, plugin_path)

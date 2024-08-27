import os.path
import uuid
import dataclasses
from typing import Union
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
from PySide6.QtCore import Signal
from PySide6.QtCore import QThreadPool

from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QToolButton
from PySide6.QtWidgets import QHBoxLayout

from pieapp.api.registries.snapshots.manager import Snapshots
from pieapp.utils.files import delete_files
from converter.widgets.submitdialog import SubmitConvertDialog

from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.plugins.decorators import on_plugin_shutdown
from pieapp.api.plugins.mixins import CoreAccessorsMixin
from pieapp.api.plugins.mixins import LayoutAccessorsMixins

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.models import Scope
from pieapp.api.models.layouts import Layout
from pieapp.api.converter.models import MediaFile
from pieapp.api.converter.constants import AUDIO_EXTENSIONS

from pieapp.api.models.indexes import Index
from pieapp.api.models.menus import MainMenu
from pieapp.api.models.menus import MainMenuItem
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.toolbar import ToolBarItem
from pieapp.api.models.statusbar import MessageStatus
from pieapp.api.models.themes import ThemeProperties, IconName

from pieapp.utils.logger import logger
from pieapp.widgets.waitingspinner import create_wait_spinner

from pieapp.api.converter.workers import ProbeWorker
from pieapp.api.converter.workers import ConverterWorker
from pieapp.api.converter.workers import CopyFilesWorker
from pieapp.api.converter.observers import FileSystemWatcher

from converter.models import ConverterThemeProperties
from converter.confpage import ConverterConfigPage

from converter.widgets.search import ConverterSearch
from converter.widgets.item import ConverterItem
from converter.widgets.list import ConverterListWidget


class Converter(PiePlugin, CoreAccessorsMixin, LayoutAccessorsMixins):
    name = SysPlugin.Converter
    requires = [SysPlugin.MainToolBar, SysPlugin.Preferences, SysPlugin.Layout, SysPlugin.Shortcut]
    optional = [SysPlugin.MainMenuBar, SysPlugin.StatusBar]

    # Emit on converter table item added to list
    sig_table_item_added = Signal(MediaFile, int)

    # Emit on snapshot created
    sig_on_snapshot_created = Signal(MediaFile)

    # Emit on snapshot deleted
    sig_on_snapshot_deleted = Signal(MediaFile)

    # Emit on snapshot modified
    sig_on_snapshot_modified = Signal(MediaFile)

    # Emit on global snapshot restored
    sig_on_snapshot_restored = Signal()

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon(IconName.App)

    @staticmethod
    def get_config_page() -> ConverterConfigPage:
        return ConverterConfigPage()

    def on_main_window_show(self) -> None:
        last_opened_folder = self.get_config("folders.last_opened_folder", Scope.User, os.path.expanduser("~"))
        self.update_config(
            "workflow.last_opened_folder",
            Scope.User,
            last_opened_folder,
            temp=True
        )

    def on_main_window_close(self) -> None:
        last_opened_folder = self.get_config("workflow.last_opened_folder", Scope.User)
        last_opened_folder = Path(last_opened_folder).parent
        last_opened_folder = str(last_opened_folder)
        self.update_config(
            "folders.last_opened_folder",
            Scope.User,
            last_opened_folder,
            save=True
        )

    def init(self) -> None:
        # Get configurations
        self._supported_formats = ""
        for audio_extension in AUDIO_EXTENSIONS:
            self._supported_formats += f"*.{audio_extension};"
        self._supported_formats = f"{translate('Supported audio formats')} - ({self._supported_formats})"

        self._temp_directory = Path(self.get_config("workflow.temp_directory", Scope.User))
        self._output_directory = Path(self.get_config("workflow.output_directory", Scope.User))
        self._chunk_size = self.get_config("ffmpeg.chunk_size", Scope.User, 10)
        self._ffmpeg_command = Path(self.get_config("ffmpeg.ffmpeg", Scope.User, "ffmpeg"))
        self._ffprobe_command = Path(self.get_config("ffmpeg.ffprobe", Scope.User, "ffprobe"))

        # Connect snapshot signals
        self._connect_snapshot_signals()
        # Setup FS watcher
        self._watcher = FileSystemWatcher(self)
        self._watcher.connect_signals(self)

        # Setup layouts and widgets
        self._converter_item_widgets: list[ConverterItem] = []
        self._quick_action_items: list[dict[str, QToolButton]] = []
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

    def _connect_snapshot_signals(self) -> None:
        """
        Connect SnapshotRegistry to proxy methods
        """
        Snapshots.sig_on_snapshot_created.connect(self._on_snapshot_created)
        Snapshots.sig_on_snapshot_deleted.connect(self._on_snapshot_deleted)
        Snapshots.sig_on_snapshot_modified.connect(self._on_snapshot_modified)
        Snapshots.sig_on_snapshot_restored.connect(self._on_snapshot_restored)

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
        icon: "QIcon",
        callback: callable = None,
        before: str = None,
        after: str = None,
        enabled: bool = True
    ) -> None:
        """
        A proxy method to add an item in the QuickActionMenu
        """
        for index, item in enumerate(self._converter_item_widgets):
            tool_button = item.add_quick_action(name, text, icon, callback, before, after, enabled)
            self._quick_action_items.insert(index, {name: tool_button})

    # Protected widget methods

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
                color_props=self.get_theme_property(ConverterThemeProperties.ConverterItemColors),
                sig_on_snapshot_modified=self.sig_on_snapshot_modified
            )

            # Add default buttons
            widget.add_quick_action(
                name="delete",
                text=translate("Delete"),
                icon=self.get_svg_icon(IconName.Delete, prop=ThemeProperties.ErrorColor),
                callback=self._delete_tool_button_connect,
                enabled=True
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
            self.sig_table_item_added.emit(media_file, index)

        self.get_tool_button(self.name, ToolBarItem.Clear).set_enabled(True)

    # ConverterListWidget protected methods

    def _content_list_item_removed(self) -> None:
        """
        Disable `clear` button on empty `content_list`
        """
        if self._content_list.count() == 0:
            self.get_tool_button(self.name, ToolBarItem.Clear).set_enabled(False)

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
        delete_files(Snapshots.values(as_path=True))
        Snapshots.restore()

        self._converter_item_widgets = []
        self._content_list.clear()

        self._list_grid_layout.remove_widget(self._search)
        self._list_grid_layout.remove_widget(self._content_list)
        self._set_placeholder()
        self.get_tool_button(self.name, ToolBarItem.Clear).set_enabled(False)

    def _delete_tool_button_connect(self, media_file_name: str) -> None:
        media_file: MediaFile = Snapshots.get(media_file_name)
        delete_files([media_file.path])

    # ConverterSearch protected methods

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

    # Public methods

    def open_files(self) -> None:
        last_opened_folder = self.get_config(
            "workflow.last_opened_folder",
            Scope.User,
            os.path.expanduser("~")
        )
        last_opened_folder = str(last_opened_folder)
        selected_files = QFileDialog.get_open_file_names(
            caption=translate("Open files"),
            dir=last_opened_folder,
            filter=self._supported_formats
        )
        selected_files = selected_files[0]
        if not selected_files:
            return

        selected_files = list(map(Path, selected_files))
        last_opened_folder = selected_files[0]
        self.update_config("workflow.last_opened_folder", Scope.User, last_opened_folder, temp=True)

        copy_files_worker = CopyFilesWorker(selected_files, self._temp_directory)
        copy_files_worker.signals.failed.connect(self._copy_files_worker_failed)
        copy_files_worker.signals.completed.connect(lambda: self._copy_files_worker_finished(selected_files))
        copy_files_worker.signals.destroyed.connect(self.destroyed)

        pool = QThreadPool.global_instance()
        pool.start(copy_files_worker)

    # File system events methods

    @Slot(Path, bool)
    def on_file_created(self, file_path: Path, is_directory: bool) -> None:
        # TODO: Display notification that new file was added if `media_file` is directory
        #       Then process new files via ConverterProbeWorker
        # self._start_converter_worker([file_path])
        pass

    @Slot(Path, str, bool)
    def on_file_moved(self, file_path: Path, new_media_file: str, is_directory: bool) -> None:
        # TODO: Show message that files were moved and user need to do something about it
        media_file = Snapshots.get(f"{file_path.parts[-2]}/{file_path.name}")
        Snapshots.update(media_file.name, new_media_file)

    @Slot(Path, bool)
    def on_file_deleted(self, file_path: Path, is_directory: bool) -> None:
        media_file_name = f"{file_path.parts[-2]}/{file_path.name}"
        if not Snapshots.contains(media_file_name):
            # Ignore `watchdog` emitting multiple events
            return

        media_file = Snapshots.get(media_file_name)
        index = Snapshots.index(media_file.name)
        Snapshots.remove(media_file.name)
        self._content_list.take_item(index)

    @Slot(Path, bool)
    def on_file_modified(self, file_path: Path, is_directory: bool) -> None:
        # TODO: Process modified file via ConverterProbeWorker
        if is_directory:
            return

        media_file_name = f"{file_path.parts[-2]}/{file_path.name}"
        if not Snapshots.contains(media_file_name):
            # Ignore this event after we deleted file(-s)
            return

        media_file = Snapshots.get(media_file_name)
        Snapshots.update(media_file.name, media_file, Index.End)

    # CopyFilesWorker handlers

    def _copy_files_worker_finished(self, selected_files: list[Path]) -> None:
        """
        Start `ConverterProbeWorker` with selected files after `CopyFilesWorker` is finished
        """
        selected_media_files = []
        for selected_file in selected_files:
            media_file = MediaFile(
                uuid=str(uuid.uuid4()),
                name=f"{selected_file.parts[-2]}/{selected_file.name}",
                path=Path(selected_file),
                output_path=self._output_directory / selected_file.name,
                is_origin=True
            )
            selected_media_files.append(media_file)

        for index, media_file in enumerate(selected_media_files):
            if media_file.name not in Snapshots:
                Snapshots.add(media_file)
            else:
                del selected_media_files[index]

        self._start_probe_worker(selected_media_files)

    @Slot(Exception)
    def _copy_files_worker_failed(self, exception: Exception):
        self._spinner.stop()
        status_bar = get_plugin(SysPlugin.StatusBar)
        if status_bar:
            status_bar.show_message(f'{translate("Failed to copy files")}: {exception!s}', MessageStatus.Error)

    def _start_probe_worker(self, media_files) -> None:
        probe_worker = ProbeWorker(
            media_files=media_files,
            temp_folder=self._temp_directory,
            ffmpeg_command=self._ffmpeg_command,
            ffprobe_command=self._ffprobe_command,
        )
        probe_worker.signals.started.connect(self._probe_worker_started)
        probe_worker.signals.completed.connect(self._probe_worker_finished)
        probe_worker.signals.failed.connect(self._probe_worker_failed)
        probe_worker.signals.destroyed.connect(self.destroyed)

        pool = QThreadPool.global_instance()
        pool.start(probe_worker)

    # ProbeWorker handlers

    def _probe_worker_started(self) -> None:
        self._clear_placeholder()
        self._list_grid_layout.add_widget(self._spinner, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._spinner.start()

    @Slot(Path)
    def _probe_worker_finished(self, models_list: list[MediaFile]) -> None:
        self._watcher.start(str(self._temp_directory))
        self._spinner.stop()

        if not self._list_grid_layout.find_child(self._spinner.__class__, self._spinner.object_name()):
            self._spinner.set_visible(False)

        self._fill_content_list(models_list)

        status_bar = get_plugin(SysPlugin.StatusBar)
        if status_bar:
            status_bar.show_message(translate(f"Loaded %s files", len(models_list)), MessageStatus.Info)

    @Slot(Exception)
    def _probe_worker_failed(self, exception: Exception) -> None:
        self._spinner.stop()
        status_bar = get_plugin(SysPlugin.StatusBar)
        if status_bar:
            status_bar.show_message(f'{translate("Failed to process files")}: {exception!s}', MessageStatus.Error)

    def _open_submit_convert_dialog(self) -> None:
        # SubmitConvertDialog(Snapshots.values()[0].path, self._start_converter_process_worker)
        SubmitConvertDialog(None, self._start_converter_worker)

    # ConverterWorker handlers

    @Slot(Path)
    def _start_converter_worker(self, output_folder: Path) -> None:
        media_files = Snapshots.values()
        converter_worker = ConverterWorker(media_files, self._ffmpeg_command)
        converter_worker.signals.started.connect(self._converter_worker_started)
        converter_worker.signals.failed.connect(self._converter_worker_failed)
        converter_worker.signals.completed.connect(self._converter_worker_finished)

        pool = QThreadPool.global_instance()
        pool.start(converter_worker)

    @Slot()
    def _converter_worker_finished(self) -> None:
        logger.debug("Finished")

    @Slot()
    def _converter_worker_started(self) -> None:
        pass

    @Slot(Exception, int)
    def _converter_worker_failed(self, exception: Exception, index: int) -> None:
        pass

    # SnapshotRegistry protected proxy methods

    @Slot(MediaFile)
    def _on_snapshot_created(self, snapshot: MediaFile) -> None:
        self.sig_on_snapshot_created.emit(snapshot)
        if len(Snapshots.values()) > 0:
            self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(True)

    @Slot(MediaFile)
    def _on_snapshot_modified(self, snapshot: MediaFile) -> None:
        self.sig_on_snapshot_modified.emit(snapshot)
        if len(Snapshots.values()) > 0:
            self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(True)

    @Slot(MediaFile)
    def _on_snapshot_deleted(self, snapshot: MediaFile) -> None:
        self.sig_on_snapshot_deleted.emit(snapshot)
        convert_button = self.get_tool_button(self.name, ToolBarItem.Convert)
        if Snapshots.count() > 0:
            convert_button.set_enabled(True)
        else:
            convert_button.set_enabled(False)

    @Slot(MediaFile)
    def _on_snapshot_restored(self) -> None:
        self.sig_on_snapshot_restored.emit()
        self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(False)

    # Debug methods

    def _debug_print_values(self) -> None:
        Snapshots.values()

    def _debug_print_metadata(self) -> None:
        snapshots = Snapshots.values()
        for snapshot in snapshots:
            for field, value in dataclasses.asdict(snapshot.metadata).items():
                logger.debug(f"{field} - {value}")

    # Shortcut methods

    def _undo_button_connect(self) -> None:
        Snapshots.update_global_snapshot_index(-1)

    def _redo_button_connect(self) -> None:
        Snapshots.update_global_snapshot_index(+1)

    # Plugin event method

    @on_plugin_available(plugin=SysPlugin.Layout)
    def _on_layout_manager_available(self) -> None:
        layout_manager = get_plugin(SysPlugin.Layout)
        main_layout = layout_manager.get_layout(Layout.Main)
        if main_layout:
            layout_manager.add_layout(self.name, main_layout,
                                      self._list_grid_layout, 0, 0, Qt.AlignmentFlag.AlignVCenter)

    @on_plugin_available(plugin=SysPlugin.Shortcut)
    def _on_shortcut_manager_available(self) -> None:
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
        shortcut.add_shortcut(
            name="debug.print_metadata",
            shortcut="Ctrl+D",
            target=self._content_list,
            triggered=self._debug_print_metadata,
            title=translate("Print snapshots"),
            description=translate("Print snapshots"),
            hidden=True
        )
        shortcut.add_shortcut(
            name="debug.print_values",
            shortcut="Ctrl+L",
            target=self._content_list,
            triggered=self._debug_print_values,
            title=translate("Print values"),
            description=translate("Print values"),
            hidden=True
        )

    @on_plugin_available(plugin=SysPlugin.Preferences)
    def _on_preferences_available(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.register_config_page(self)

    @on_plugin_shutdown(plugin=SysPlugin.Preferences)
    def _on_preferences_teardown(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.deregister_config_page(self)

    @on_plugin_available(plugin=SysPlugin.MainMenuBar)
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
            icon=self.get_svg_icon(IconName.FolderOpen),
            index=Index.Start,
            triggered=self.open_files
        )

    @on_plugin_available(plugin=SysPlugin.MainToolBar)
    def _on_toolbar_available(self) -> None:
        """
        Add tool button on the `Workbench`
        """
        self.add_tool_button(
            scope=self.name,
            name=ToolBarItem.OpenFiles,
            text=translate("Open file"),
            tooltip=translate("Open file"),
            icon=self.get_svg_icon(IconName.Folder),
            triggered=self.open_files
        )

        convert_tool_button = self.add_tool_button(
            scope=self.name,
            name=ToolBarItem.Convert,
            text=translate("Convert"),
            tooltip=translate("Convert"),
            icon=self.get_svg_icon(IconName.Bolt)
        )
        convert_tool_button.set_enabled(False)
        convert_tool_button.clicked.connect(self._start_converter_worker)

        clear_tool_button = self.add_tool_button(
            scope=self.name,
            name=ToolBarItem.Clear,
            text=translate("Clear"),
            tooltip=translate("Click to clear list of files"),
            icon=self.get_svg_icon(IconName.Delete)
        )
        clear_tool_button.set_enabled(False)
        clear_tool_button.clicked.connect(self._clear_content_list)

        self.add_toolbar_item(
            toolbar=SysPlugin.MainToolBar,
            name=ToolBarItem.OpenFiles,
            item=self.get_tool_button(self.name, ToolBarItem.OpenFiles),
        )

        self.add_toolbar_item(
            toolbar=SysPlugin.MainToolBar,
            name=ToolBarItem.Convert,
            item=self.get_tool_button(self.name, ToolBarItem.Convert),
            after=ToolBarItem.OpenFiles
        )

        self.add_toolbar_item(
            toolbar=SysPlugin.MainToolBar,
            name=ToolBarItem.Clear,
            item=self.get_tool_button(self.name, ToolBarItem.Clear),
            after=ToolBarItem.Convert
        )


def main(parent: "QMainWindow", plugin_path: "Path"):
    return Converter(parent, plugin_path)

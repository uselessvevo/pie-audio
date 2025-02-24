from __feature__ import snake_case

import os.path
import uuid
import dataclasses
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
from PySide6.QtCore import Signal
from PySide6.QtCore import QThreadPool

from converter.widgets.mainwidget import ConverterPluginWidget
from pieapp.api.globals import Global
from pieapp.api.plugins.quickaction import QuickAction
from pieapp.api.registries.quickactions.registry import QuickActionRegistry
from pieapp.api.utils.files import delete_files
from pieapp.api.utils.files import delete_directory
from pieapp.api.utils.files import create_temp_directory
from pieapp.api.utils.files import create_output_directory

from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.plugins.decorators import on_plugin_shutdown

from pieapp.api.plugins.mixins import CoreAccessorsMixin, WidgetsAccessorMixins

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.snapshots.registry import SnapshotRegistry

from pieapp.api.models.scopes import Scope
from pieapp.api.models.layouts import Layout
from pieapp.api.converter.models import MediaFile

from pieapp.api.models.indexes import Index
from pieapp.api.models.menus import MainMenu
from pieapp.api.models.menus import MainMenuItem
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.toolbars import ToolBarItem
from pieapp.api.models.statusbars import MessageStatus
from pieapp.api.models.themes import ThemeProperties, IconName

from pieapp.api.utils.logger import logger
from pieapp.api.utils.qapp import get_application
from pieapp.widgets.buttons import Button, ButtonRole
from pieapp.widgets.messagebox import MessageBox

from pieapp.api.converter.workers import ProbeWorker
from pieapp.api.converter.workers import ConverterWorker
from pieapp.api.converter.workers import CopyFilesWorker
from pieapp.api.converter.observers import FileSystemWatcher

from converter.confpage import ConverterConfigPage


class Converter(PiePlugin, CoreAccessorsMixin, WidgetsAccessorMixins):
    name = SysPlugin.Converter
    requires = [
        SysPlugin.MainToolBar,
        SysPlugin.StatusBar,
        SysPlugin.Preferences,
        SysPlugin.Layout,
        SysPlugin.ShortcutManager
    ]
    optional = [SysPlugin.MainMenuBar]
    widget_class = ConverterPluginWidget

    sig_files_ready = Signal()

    # Emit on converter table item added to list
    sig_table_item_added = Signal(MediaFile)

    # Emit on snapshot created
    sig_snapshot_created = Signal(MediaFile)

    # Emit on snapshot deleted
    sig_snapshot_deleted = Signal(MediaFile)

    # Emit on snapshot modified
    sig_snapshot_modified = Signal(MediaFile)

    # Emit on global snapshot restored
    sig_snapshots_restored = Signal()

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon(IconName.App, self.name)

    @staticmethod
    def get_title() -> str:
        return translate("Converter")

    @staticmethod
    def get_description() -> str:
        return translate("Converter")

    def on_before_main_window_show(self) -> None:
        self._connect_snapshot_signals()
        self._watcher = FileSystemWatcher(self)
        self._watcher.connect_signals(self)

    def on_main_window_show(self) -> None:
        # Prepare output directory
        output_directory = self.get_app_config("workflow.output_directory", Scope.User)
        if output_directory is None or Path(output_directory).exists() is False:
            output_directory = create_output_directory(output_directory)
            self.update_app_config(
                "workflow.output_directory",
                Scope.User,
                str(output_directory)
            )

        last_opened_directory = self.get_app_config(
            "workflow.last_opened_directory",
            Scope.User,
            os.path.expanduser("~")
        )
        self.update_app_config(
            "workflow.last_opened_directory",
            Scope.User,
            last_opened_directory
        )

        # Prepare temp directory

        temp_directory = self.get_app_config("workflow.temp_directory", Scope.User)
        if temp_directory is not None and Path(temp_directory).exists() is True:
            temp_directory = Path(temp_directory)
            message_box = MessageBox(
                parent=self._parent,
                yes_button_text=translate("Restore"),
                no_button_text=translate("Discard"),
                window_title=translate("Restore session?"),
                message_text=translate("You have unsaved files from your previous session.\n"
                                       "Would you like to restore them, or start fresh?"),
                show_checkbox=False,
                show_close_button=False
            )
            message_box.set_style_sheet("QLabel{min-width: 420; min-height: 100}")

            close_app_button = Button(ButtonRole.Flat)
            close_app_button.set_text(translate("Quit"))
            message_box.add_button(close_app_button, MessageBox.ButtonRole.ActionRole)

            message_box.exec()
            message_box_reply = message_box.button_role(message_box.clicked_button())
            if message_box_reply == MessageBox.ButtonRole.ActionRole:
                get_application().exit()

            elif message_box_reply == MessageBox.ButtonRole.YesRole:
                selected_files = []
                for file in Path(temp_directory).iterdir():
                    if file.suffix.replace(".", "") in Global.AUDIO_EXTENSIONS:
                        selected_files.append(file)
                self.start_copy_files_worker(selected_files)

            elif message_box_reply == MessageBox.ButtonRole.NoRole:
                delete_directory(temp_directory)
                delete_files(list(temp_directory.rglob("*.*")))

        self.save_app_config("workflow", Scope.User)

    def on_main_window_close(self) -> None:
        self.save_app_config("workflow", Scope.User)

    def _connect_snapshot_signals(self) -> None:
        SnapshotRegistry.sig_snapshot_created.connect(self._on_snapshot_created)
        SnapshotRegistry.sig_snapshot_modified.connect(self._on_snapshot_modified)
        SnapshotRegistry.sig_snapshot_deleted.connect(self._on_snapshots_deleted)
        SnapshotRegistry.sig_snapshots_restored.connect(self._on_snapshots_restored)

    def connect_widget_signals(self) -> None:
        widget = self.get_widget()
        widget.sig_files_selected.connect(self.on_files_selected)
        widget.sig_snapshot_deleted.connect(self._on_snapshots_deleted)
        widget.sig_table_item_added.connect(self._on_table_item_added)

    def init(self) -> None:
        # Prepare workflow variables
        self.chunk_size = self.get_app_config("ffmpeg.chunk_size", Scope.User, 10)
        self.ffmpeg_command = Path(self.get_app_config("ffmpeg.ffmpeg", Scope.User, "ffmpeg"))
        self.ffprobe_command = Path(self.get_app_config("ffmpeg.ffprobe", Scope.User, "ffprobe"))
        self.connect_widget_signals()

    # QuickAction public proxy methods

    def register_quick_action(self, quick_action: QuickAction) -> None:
        """
        A proxy method to add an item in the QuickActionMenu
        """
        QuickActionRegistry.add(quick_action)

    def deregister_quick_action(self, index: int, name: str):
        pass

    def update_quick_action(self, index: int, name: str):
        pass

    def toggle_quick_action(self, index: int, name: str):
        pass

    # Protected widget methods

    def clear_content_list(self) -> None:
        """
        Clear content list, remove it from the `list_grid_layout` and disable clear button
        """
        delete_files(SnapshotRegistry.values(as_path=True))
        SnapshotRegistry.restore()
        self.get_widget().clear_content_list()

    # Public methods

    @Slot(list)
    def on_files_selected(self, selected_files: list[str]) -> None:
        temp_directory = create_temp_directory(Global.USER_ROOT / Global.DEFAULT_TEMP_DIR_NAME)
        self.update_app_config(
            "workflow.temp_directory",
            Scope.User,
            str(temp_directory)
        )

        selected_files = list(map(Path, selected_files))
        last_opened_directory = selected_files[0]
        self.update_app_config("workflow.last_opened_directory", Scope.User, last_opened_directory, temp=True)
        self.start_copy_files_worker(selected_files)

    def start_copy_files_worker(self, files: list[Path]) -> None:
        if len(files) == 0:
            status_bar = get_plugin(SysPlugin.StatusBar)
            if status_bar:
                status_bar.show_message(translate("No files were found"), MessageStatus.Error)
            return

        temp_directory = Path(self.get_app_config("workflow.temp_directory", Scope.User))
        copy_files_worker = CopyFilesWorker(files, temp_directory)
        copy_files_worker.signals.failed.connect(self.copy_files_worker_failed)
        copy_files_worker.signals.completed.connect(lambda: self.copy_files_worker_finished(files))
        copy_files_worker.signals.destroyed.connect(self.destroyed)

        pool = QThreadPool.global_instance()
        pool.start(copy_files_worker)

    # File system events methods

    @Slot(Path, bool)
    def on_file_created(self, file_path: Path, is_directory: bool) -> None:
        # Ignore directories and manually added files
        if is_directory:
            return

        media_file = SnapshotRegistry.get(f"{file_path.parts[-2]}/{file_path.name}")
        index = len(SnapshotRegistry.values())
        self.get_widget().on_file_created(index, media_file)

    @Slot(Path, str, bool)
    def on_file_moved(self, file_path: Path, new_media_file: str, is_directory: bool) -> None:
        media_file = SnapshotRegistry.get(f"{file_path.parts[-2]}/{file_path.name}")
        SnapshotRegistry.update(media_file.name, media_file)
        index = SnapshotRegistry.index(media_file.name)
        self.get_widget().on_file_moved(index, new_media_file)

    @Slot(Path, bool)
    def on_file_deleted(self, file_path: Path, is_directory: bool) -> None:
        media_file_name = f"{file_path.parts[-2]}/{file_path.name}"
        if not SnapshotRegistry.contains(media_file_name):
            # Ignore `watchdog` emitting multiple events
            return

        media_file = SnapshotRegistry.get(media_file_name)
        index = SnapshotRegistry.index(media_file.name)
        SnapshotRegistry.remove(media_file.name)
        self.get_widget().on_file_deleted(index)

    @Slot(Path, bool)
    def on_file_modified(self, file_path: Path, is_directory: bool) -> None:
        # TODO: Process modified file via ConverterProbeWorker
        if is_directory:
            return

        media_file_name = f"{file_path.parts[-2]}/{file_path.name}"
        if not SnapshotRegistry.contains(media_file_name):
            # Ignore this event after we deleted file(-s)
            return

        media_file = SnapshotRegistry.get(media_file_name)
        SnapshotRegistry.update(media_file.name, media_file, Index.End)
        index = SnapshotRegistry.get(media_file_name)
        self.get_widget().on_file_modified(index, media_file)

    # SnapshotRegistry protected proxy methods

    @Slot(MediaFile)
    def _on_snapshot_created(self, snapshot: MediaFile) -> None:
        self.get_widget().on_snapshot_created()

    @Slot(MediaFile)
    def _on_snapshot_modified(self, snapshot: MediaFile) -> None:
        index = SnapshotRegistry.index(snapshot.name)
        self.get_widget().on_snapshot_modified(index, snapshot)

    @Slot(MediaFile)
    def _on_snapshots_deleted(self, snapshot: MediaFile) -> None:
        index = SnapshotRegistry.index(snapshot.name)
        self.get_widget().on_snapshot_deleted(index, snapshot)

    @Slot(MediaFile)
    def _on_snapshots_restored(self) -> None:
        self.get_widget().on_snapshots_restored()

    # CopyFilesWorker handlers

    def copy_files_worker_finished(self, selected_files: list[Path]) -> None:
        """
        Start `ConverterProbeWorker` with selected files after `CopyFilesWorker` is finished
        """
        output_directory = self.get_app_config("workflow.output_directory", Scope.User)
        output_directory = Path(output_directory)
        selected_media_files = []
        for selected_file in selected_files:
            media_file = MediaFile(
                uuid=str(uuid.uuid4()),
                name=f"{selected_file.parts[-2]}/{selected_file.name}",
                path=Path(selected_file),
                output_path=output_directory / selected_file.name
            )
            selected_media_files.append(media_file)

        for index, media_file in enumerate(selected_media_files):
            if media_file.name not in SnapshotRegistry:
                SnapshotRegistry.add(media_file)
            else:
                del selected_media_files[index]

        self.start_probe_worker(selected_media_files)

    @Slot(Exception)
    def copy_files_worker_failed(self, exception: Exception):
        self.get_widget().copy_files_worker_failed()
        status_bar = get_plugin(SysPlugin.StatusBar)
        if status_bar:
            status_bar.show_message(f'{translate("Failed to copy files")}: {exception!s}', MessageStatus.Error)

    def start_probe_worker(self, media_files) -> None:
        probe_worker = ProbeWorker(
            media_files=media_files,
            temp_folder=Path(self.get_app_config("workflow.temp_directory", Scope.User)),
            ffmpeg_command=self.ffmpeg_command,
            ffprobe_command=self.ffprobe_command,
        )
        probe_worker.signals.started.connect(self.probe_worker_started)
        probe_worker.signals.completed.connect(self.probe_worker_finished)
        probe_worker.signals.failed.connect(self.probe_worker_failed)
        probe_worker.signals.destroyed.connect(self.destroyed)

        pool = QThreadPool.global_instance()
        pool.start(probe_worker)

    # ProbeWorker handlers

    def probe_worker_started(self) -> None:
        self.get_widget().probe_worker_started()

    @Slot(Path)
    def probe_worker_finished(self, models_list: list[MediaFile]) -> None:
        self._watcher.start(self.get_app_config("workflow.temp_directory", Scope.User))
        self.get_widget().probe_worker_finished()
        self.get_widget().render_quick_actions(models_list)

        status_bar = get_plugin(SysPlugin.StatusBar)
        if status_bar:
            status_bar.show_message(translate(f"Loaded %s files", len(models_list)), MessageStatus.Info)

    @Slot(Exception)
    def probe_worker_failed(self, exception: Exception) -> None:
        self.get_widget().probe_worker_failed()
        status_bar = get_plugin(SysPlugin.StatusBar)
        if status_bar:
            status_bar.show_message(f'{translate("Failed to process files")}: {exception!s}', MessageStatus.Error)

    # ConverterWorker handlers

    @Slot(Path)
    def start_converter_worker(self, output_folder: Path) -> None:
        media_files = SnapshotRegistry.values()
        converter_worker = ConverterWorker(media_files, self.ffmpeg_command)
        converter_worker.signals.started.connect(self.converter_worker_started)
        converter_worker.signals.failed.connect(self.converter_worker_failed)
        converter_worker.signals.completed.connect(self.converter_worker_finished)

        pool = QThreadPool.global_instance()
        pool.start(converter_worker)

    # ConverterWorker handlers

    @Slot()
    def converter_worker_started(self) -> None:
        pass

    @Slot()
    def converter_worker_finished(self) -> None:
        logger.debug("Finished")

    @Slot(Exception, int)
    def converter_worker_failed(self, exception: Exception, index: int) -> None:
        pass

    # Debug methods

    def debug_print_values(self) -> None:
        SnapshotRegistry.values()

    def debug_print_metadata(self) -> None:
        snapshots = SnapshotRegistry.values()
        for snapshot in snapshots:
            for field, value in dataclasses.asdict(snapshot.metadata).items():
                logger.debug(f"{field} - {value}")

    # Shortcut methods

    def undo_button_connect(self) -> None:
        SnapshotRegistry.update_global_snapshot_index(-1)

    def redo_button_connect(self) -> None:
        SnapshotRegistry.update_global_snapshot_index(+1)

    # Widget methods

    def _on_table_item_added(self, media_file: MediaFile) -> None:
        self.sig_table_item_added.emit(media_file)

    # Plugin event methods

    @on_plugin_available(plugin=SysPlugin.Layout)
    def on_layout_manager_available(self) -> None:
        widget = self.get_widget()
        layout_manager = get_plugin(SysPlugin.Layout)
        main_layout = layout_manager.get_layout(Layout.Main)
        if main_layout:
            main_layout.add_layout(widget.get_main_layout(), 0, 0, Qt.AlignmentFlag.AlignCenter)
            layout_manager.add_layout(self.name, widget.get_main_layout(), Layout.Main)

    @on_plugin_available(plugin=SysPlugin.Preferences)
    def on_preferences_available(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.register_config_page(ConverterConfigPage)

    @on_plugin_shutdown(plugin=SysPlugin.Preferences)
    def on_preferences_teardown(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.deregister_config_page(ConverterConfigPage)

    @on_plugin_available(plugin=SysPlugin.ShortcutManager)
    def on_shortcut_manager_available(self) -> None:
        widget = self.get_widget()
        self.add_shortcut(
            name="open_files",
            shortcut="Ctrl+O",
            triggered=widget.open_files,
            target=self.parent(),
            title=translate("Open files"),
            description=translate("Open files to process them")
        )
        self.add_shortcut(
            name="toggle_search",
            shortcut="Ctrl+F",
            triggered=widget.toggle_search,
            target=widget.content_list_widget,
            title=translate("Toggle search input"),
            description=translate("Toggle search input in converter content list")
        )
        self.add_shortcut(
            name="media_file.undo",
            shortcut="Ctrl+Z",
            target=widget.content_list_widget,
            triggered=self.undo_button_connect,
            title=translate("Undo"),
            description=translate("Undo file state"),
            hidden=True
        )
        self.add_shortcut(
            name="media_file.redo",
            shortcut="Ctrl+Y",
            target=widget.content_list_widget,
            triggered=self.redo_button_connect,
            title=translate("Redo"),
            description=translate("Redo file state"),
            hidden=True
        )
        if Global.IS_DEBUG:
            self.add_shortcut(
                name="debug.print_metadata",
                shortcut="Ctrl+D",
                target=widget.content_list_widget,
                triggered=self.debug_print_metadata,
                title=translate("Print snapshots"),
                description=translate("Print snapshots"),
                hidden=True
            )
            self.add_shortcut(
                name="debug.print_values",
                shortcut="Ctrl+L",
                target=widget.content_list_widget,
                triggered=self.debug_print_values,
                title=translate("Print values"),
                description=translate("Print values"),
                hidden=True
            )

    @on_plugin_available(plugin=SysPlugin.MainMenuBar)
    def on_menu_bar_available(self) -> None:
        """
        Add open file element in the "File" menu
        """
        self.add_menu_item(
            scope=Scope.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.OpenFiles,
            text=translate("Open file"),
            icon=self.get_svg_icon(IconName.FolderOpen),
            index=Index.Start,
            triggered=self.get_widget().open_files
        )

    @on_plugin_available(plugin=SysPlugin.MainToolBar)
    def on_toolbar_available(self) -> None:
        """
        Add tool button on the `Workbench`
        """
        self.add_tool_button(
            scope=self.name,
            name=ToolBarItem.OpenFiles,
            text=translate("Open file"),
            tooltip=translate("Open file"),
            icon=self.get_svg_icon(IconName.Folder),
            triggered=self.get_widget().open_files
        )

        convert_tool_button = self.add_tool_button(
            scope=self.name,
            name=ToolBarItem.Convert,
            text=translate("Convert"),
            tooltip=translate("Convert"),
            icon=self.get_svg_icon(IconName.Bolt)
        )
        convert_tool_button.set_enabled(False)
        convert_tool_button.clicked.connect(self.start_converter_worker)

        clear_tool_button = self.add_tool_button(
            scope=self.name,
            name=ToolBarItem.Clear,
            text=translate("Clear"),
            tooltip=translate("Click to clear list of files"),
            icon=self.get_svg_icon(IconName.Delete)
        )
        clear_tool_button.set_enabled(False)
        clear_tool_button.clicked.connect(self.clear_content_list)

        self.add_toolbar_item(
            toolbar_name=SysPlugin.MainToolBar,
            item_name=ToolBarItem.OpenFiles,
            item_widget=self.get_tool_button(self.name, ToolBarItem.OpenFiles),
        )

        self.add_toolbar_item(
            toolbar_name=SysPlugin.MainToolBar,
            item_name=ToolBarItem.Convert,
            item_widget=self.get_tool_button(self.name, ToolBarItem.Convert),
            after=ToolBarItem.OpenFiles
        )

        self.add_toolbar_item(
            toolbar_name=SysPlugin.MainToolBar,
            item_name=ToolBarItem.Clear,
            item_widget=self.get_tool_button(self.name, ToolBarItem.Clear),
            after=ToolBarItem.Convert
        )


def main(parent, plugin_path):
    return Converter(parent, plugin_path)

from __feature__ import snake_case

import copy

from PySide6.QtCore import Slot

from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.snapshots.registry import SnapshotRegistry

from pieapp.api.models.indexes import Index
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.converter.models import update_media_file, MediaFile

from metadata.widgets.quickaction import EditQuickAction
from metadata.widgets.mainwidget import MetadataEditorWidget


class MetadataEditor(PiePlugin):
    name = SysPlugin.MetadataEditor
    widget_class = MetadataEditorWidget
    requires = [SysPlugin.Converter, SysPlugin.MainToolBar]

    def get_title(self) -> str:
        return translate("Metadata editor")

    def get_description(self) -> str:
        return translate("Metadata editor")

    def init(self) -> None:
        widget = self.get_widget()
        widget.sig_dialog_closed.connect(self._on_close_event)
        widget.sig_changes_saved.connect(self._on_save_event)
        widget.sig_table_item_changed.connect(self._on_table_item_changed)
        widget.sig_album_cover_changed.connect(self._on_album_cover_changed)

    def call(self, media_file_name: str) -> None:
        media_file = SnapshotRegistry.get(media_file_name)
        SnapshotRegistry.add_local_snapshot(media_file_name, media_file)
        self.get_widget().fill_metadata_table(media_file)
        self.get_widget().call()

    @on_plugin_available(plugin=SysPlugin.Converter)
    def on_converter_available(self) -> None:
        converter = get_plugin(SysPlugin.Converter)
        quick_action = EditQuickAction(self, enabled=False)
        converter.register_quick_action(quick_action)

    @on_plugin_available(plugin=SysPlugin.MainToolBar)
    def on_toolbar_available(self) -> None:
        self.get_widget().init_toolbar()

    def _on_undo(self, media_file_name: str) -> None:
        media_file, is_array_end = SnapshotRegistry.update_local_snapshot_index(media_file_name, -1)
        self.get_widget().on_undo(media_file, is_array_end)

    def _on_redo(self, media_file_name: str) -> None:
        media_file, is_array_end = SnapshotRegistry.update_local_snapshot_index(media_file_name, +1)
        self.get_widget().on_redo(media_file, is_array_end)

    @Slot(str, str, int)
    def _on_album_cover_changed(self, media_file_name: str, image_path: str, index: int) -> None:
        media_file_copy = copy.deepcopy(SnapshotRegistry.get_local_snapshot(media_file_name, index))
        # TODO: Save different image sizes
        media_file_copy = update_media_file(
            media_file_copy,
            "metadata.album_cover.image_path",
            image_path
        )
        self.get_widget().change_tool_buttons_state(media_file_copy)

    @Slot(str, str, str)
    def _on_table_item_changed(self, media_file_name: str, field: str, value: str) -> None:
        media_file_name = media_file_name
        media_file_copy = copy.deepcopy(SnapshotRegistry.get_local_snapshot(media_file_name, Index.End))
        media_file_copy = update_media_file(media_file_copy, field, value)
        if not SnapshotRegistry.contains_local(media_file_copy.name, media_file_copy):
            SnapshotRegistry.add_local_snapshot(media_file_copy.name, media_file_copy)
            self.get_widget().change_tool_buttons_state()

    @Slot(str)
    def _on_save_event(self, media_file_name: str) -> None:
        local_snapshot = SnapshotRegistry.get_local_snapshot(media_file_name, Index.End)
        SnapshotRegistry.sync_local_to_global(local_snapshot.name)

    @Slot(str)
    def _on_close_event(self, media_file_name: str) -> None:
        SnapshotRegistry.sync_global_to_inner()
        SnapshotRegistry.restore_local_snapshots(media_file_name)


def main(parent, plugin_path):
    return MetadataEditor(parent, plugin_path)
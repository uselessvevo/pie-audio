import copy
from pathlib import Path

from PySide6.QtGui import Qt
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem

from metadata.widgets.quickaction import EditQuickAction
from pieapp.api.globals import Global
from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.plugins.mixins import DialogWidgetMixin, CoreAccessorsMixin
from pieapp.api.plugins.quickaction import QuickAction
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.snapshots.registry import SnapshotRegistry

from pieapp.api.utils.logger import logger
from pieapp.api.utils.validators import date_validator
from pieapp.widgets.delegates import ReadOnlyDelegate
from pieapp.widgets.mediatableitem import MediaTableWidgetItem

from pieapp.api.models.indexes import Index
from pieapp.api.converter.models import MediaFile, update_media_file
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.themes import ThemeProperties, IconName

from metadata.widgets.albumpicker import AlbumCoverPicker


class MetadataEditor(PiePlugin, CoreAccessorsMixin, DialogWidgetMixin):
    name = SysPlugin.MetadataEditor
    requires = [SysPlugin.Converter, SysPlugin.MainToolBar]

    @on_plugin_available(plugin=SysPlugin.Converter)
    def on_converter_available(self) -> None:
        converter = get_plugin(SysPlugin.Converter)
        quick_action = EditQuickAction(self, enabled=False)
        converter.register_quick_action(quick_action)

        self._dialog = QDialog(self._parent)
        # self._dialog.key_press_event = self._key_press_event
        self._dialog.set_object_name("MetadataEditor")
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.resize(*Global.DEFAULT_WINDOW_SIZE)

    @on_plugin_available(plugin=SysPlugin.MainToolBar)
    def on_toolbar_available(self) -> None:
        # Setup main toolbar
        main_grid_layout = QGridLayout()

        self._toolbar = self.add_toolbar(self.name)
        self._toolbar.set_fixed_height(50)
        self._toolbar.set_contents_margins(6, 0, 10, 0)
        self._toolbar.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self._toolbar.set_object_name("MetadataToolBar")

        # Setup tool buttons

        self._save_button = self.add_tool_button(
            scope=self.name,
            name="save",
            text=translate("Save"),
            tooltip=translate("Save"),
            icon=self.get_svg_icon(IconName.Save)
        )
        self._save_button.set_enabled(False)

        self._undo_button = self.add_tool_button(
            scope=self.name,
            name="undo",
            text=translate("Undo"),
            tooltip=translate("Undo"),
            icon=self.get_svg_icon(IconName.Undo)
        )
        self._undo_button.set_enabled(False)

        self._redo_button = self.add_tool_button(
            scope=self.name,
            name="redo",
            text=translate("Redo"),
            tooltip=translate("Redo"),
            icon=self.get_svg_icon(IconName.Redo)
        )
        self._redo_button.set_enabled(False)

        self.add_toolbar_item(self._toolbar.name, "save", self._save_button)
        self.add_toolbar_item(self._toolbar.name, "undo", self._undo_button)
        self.add_toolbar_item(self._toolbar.name, "redo", self._redo_button)

        # Setup table widget

        self._table_widget = QTableWidget()
        self._table_widget.set_object_name("MetadataTable")
        self._table_widget.set_row_count(15)
        self._table_widget.set_column_count(2)
        self._table_widget.vertical_header().hide()
        self._table_widget.horizontal_header().hide()
        self._table_widget.horizontal_header().set_section_resize_mode(0, QHeaderView.ResizeMode.ResizeToContents)
        self._table_widget.horizontal_header().set_section_resize_mode(1, QHeaderView.ResizeMode.Stretch)
        self._table_widget.set_item_delegate_for_column(0, ReadOnlyDelegate(self._dialog))

        main_grid_layout.add_widget(self._toolbar, 0, 0, Qt.AlignmentFlag.AlignTop)
        main_grid_layout.add_widget(self._table_widget)

        self._dialog.set_layout(main_grid_layout)

        self._toolbar.call()

    def show_editor_table(self, media_file_name: str) -> None:
        media_file: MediaFile = SnapshotRegistry.get(media_file_name)
        self._dialog.close_event = lambda event: self._close_event(event, media_file.name)
        SnapshotRegistry.add_local_snapshot(media_file.name, media_file)
        self._dialog.set_window_title(f"{translate('Edit metadata')} - {media_file.info.filename}")

        self._save_button.clicked.connect(lambda: self._save_button_connect(media_file))
        self._undo_button.clicked.connect(lambda: self._undo_button_connect(media_file))
        self._redo_button.clicked.connect(lambda: self._redo_button_connect(media_file))

        self._table_widget.set_item(0, 0, QTableWidgetItem(translate("Title")))
        self._table_widget.set_item(1, 0, QTableWidgetItem(translate("Genre")))
        self._table_widget.set_item(2, 0, QTableWidgetItem(translate("Subgenre")))
        self._table_widget.set_item(3, 0, QTableWidgetItem(translate("Track number")))
        self._table_widget.set_item(4, 0, QTableWidgetItem(translate("Cover image")))
        self._table_widget.set_item(5, 0, QTableWidgetItem(translate("Primary artist")))
        self._table_widget.set_item(6, 0, QTableWidgetItem(translate("Publisher")))
        self._table_widget.set_item(7, 0, QTableWidgetItem(translate("Explicit content")))
        self._table_widget.set_item(8, 0, QTableWidgetItem(translate("Lyrics language")))
        self._table_widget.set_item(9, 0, QTableWidgetItem(translate("Lyrics publisher")))
        self._table_widget.set_item(10, 0, QTableWidgetItem(translate("Release language")))
        self._table_widget.set_item(11, 0, QTableWidgetItem(translate("Featured artist")))
        self._table_widget.set_item(12, 0, QTableWidgetItem(translate("Additional artist")))
        self._table_widget.set_item(13, 0, QTableWidgetItem(translate("Additional contributors")))
        self._table_widget.set_item(14, 0, QTableWidgetItem(translate("Year of composition")))

        self._fill_metadata_table(media_file)
        self._dialog.show()

    def _disconnect_signals(self) -> None:
        try:
            self._table_widget.itemChanged.disconnect()
        except Exception as e:
            logger.debug(str(e))

    def _fill_metadata_table(self, media_file: MediaFile) -> None:
        # TODO: Do something about this mess
        self._disconnect_signals()
        contributors_list_widget = QListWidget()
        contributors_list_widget.itemChanged.connect(self._contributors_list_widget_changed)
        contributors_list_widget.add_items(media_file.metadata.additional_contributors)

        album_cover = media_file.metadata.album_cover
        image_path = Path(album_cover.image_path).as_posix() if Path(album_cover.image_path).exists() else None
        picker_icon = self.get_svg_icon(
            key=IconName.FolderOpen,
            prop=ThemeProperties.AppIconColor
        )
        album_cover_widget = AlbumCoverPicker(
            parent=self._dialog,
            media_file_name=media_file.name,
            image_path=image_path,
            picker_icon=picker_icon,
            placeholder_text=translate("No image selected"),
            select_album_cover_text=translate("Select album cover image")
        )
        album_cover_widget.sig_album_cover_changed.connect(self._album_cover_changed)

        self._table_widget.set_item(
            0, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.title",
                value=media_file.metadata.title
            )
        )
        self._table_widget.set_item(
            1, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.genre",
                value=media_file.metadata.genre
            )
        )
        self._table_widget.set_item(
            2, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.subgenre",
                value=media_file.metadata.subgenre
            )
        )
        self._table_widget.set_item(
            3, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.track_number",
                value=media_file.metadata.track_number
            )
        )
        self._table_widget.set_cell_widget(
            4, 1, album_cover_widget
        )
        self._table_widget.set_item(
            5, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.primary_artist",
                value=media_file.metadata.primary_artist
            )
        )
        self._table_widget.set_item(
            6, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.publisher",
                value=media_file.metadata.publisher
            )
        )
        self._table_widget.set_item(
            7, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.explicit_content",
                value=media_file.metadata.explicit_content
            )
        )
        self._table_widget.set_item(
            8, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.lyrics_language",
                value=media_file.metadata.lyrics_language
            )
        )
        self._table_widget.set_item(
            9, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.lyrics_publisher",
                value=media_file.metadata.lyrics_publisher
            )
        )
        self._table_widget.set_item(
            10, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.composition_owner",
                value=media_file.metadata.composition_owner
            )
        )
        self._table_widget.set_item(
            11, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.release_language",
                value=media_file.metadata.release_language
            )
        )
        self._table_widget.set_item(
            12, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.featured_artist",
                value=media_file.metadata.featured_artist
            )
        )
        self._table_widget.set_cell_widget(
            13, 1, contributors_list_widget
        )
        self._table_widget.set_item(
            14, 1,
            MediaTableWidgetItem(
                media_file_name=media_file.name,
                field="metadata.year_of_composition",
                value=media_file.metadata.year_of_composition,
                validators=[date_validator]
            )
        )

        self._table_widget.itemChanged.connect(self._table_item_changed)

    @Slot(int)
    def _contributors_list_widget_changed(self, index: int) -> None:
        pass

    @Slot(str, str)
    def _album_cover_changed(self, media_file_name: str, image_path: str) -> None:
        media_file_copy = copy.deepcopy(SnapshotRegistry.get_local_snapshot(media_file_name, Index.End))
        # TODO: Save different image sizes
        media_file_copy = update_media_file(
            media_file_copy,
            "metadata.album_cover.image_path",
            image_path
        )
        self._change_controls_state(media_file_copy)

    @Slot(MediaTableWidgetItem)
    def _table_item_changed(self, item: MediaTableWidgetItem) -> None:
        item = self._table_widget.item(item.row(), item.column())
        if not isinstance(item, MediaTableWidgetItem):
            return

        item.set_text(item.text())
        media_file_name = item.media_file_name
        media_file_copy = copy.deepcopy(SnapshotRegistry.get_local_snapshot(media_file_name, Index.End))
        media_file_copy = update_media_file(media_file_copy, item.field, item.value)
        self._change_controls_state(media_file_copy)

    def _change_controls_state(self, media_file: MediaFile) -> None:
        if not SnapshotRegistry.contains_local(media_file.name, media_file):
            SnapshotRegistry.add_local_snapshot(media_file.name, media_file)
            self._save_button.set_enabled(True)
            self._undo_button.set_enabled(True)
            self._redo_button.set_enabled(False)

    def _save_button_connect(self, media_file: MediaFile) -> None:
        # Sync local and global snapshots
        local_snapshot = SnapshotRegistry.get_local_snapshot(media_file.name, Index.End)
        SnapshotRegistry.sync_local_to_global(local_snapshot.name)
        self._save_button.set_enabled(False)
        self._undo_button.set_enabled(True)
        self._redo_button.set_enabled(False)

    def _undo_button_connect(self, media_file: MediaFile) -> None:
        media_file, is_array_end = SnapshotRegistry.update_local_snapshot_index(media_file.name, -1)
        self._fill_metadata_table(media_file)
        self._save_button.set_enabled(True)
        self._undo_button.set_disabled(is_array_end)
        self._redo_button.set_enabled(True)

    def _redo_button_connect(self, media_file: MediaFile) -> None:
        media_file, is_array_end = SnapshotRegistry.update_local_snapshot_index(media_file.name, +1)
        self._fill_metadata_table(media_file)
        self._save_button.set_enabled(True)
        self._undo_button.set_enabled(True)
        self._redo_button.set_disabled(is_array_end)

    def _close_event(self, _, local_snapshot_name: str) -> None:
        self._save_button.set_enabled(False)
        self._redo_button.set_enabled(False)
        self._undo_button.set_enabled(False)
        SnapshotRegistry.sync_global_to_inner()
        SnapshotRegistry.restore_local_snapshots(local_snapshot_name)

    def _key_press_event(self, event) -> None:
        if event.key() != Qt.Key.Key_Escape:
            self._dialog.key_press_event(event)


def main(parent, plugin_path):
    return MetadataEditor(parent, plugin_path)
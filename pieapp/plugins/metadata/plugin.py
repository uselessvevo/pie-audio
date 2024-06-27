from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QStyledItemDelegate

from pieapp.api.gloader import Global
from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_ready

from pieapp.api.models.media import MediaFile
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.themes import ThemeProperties

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.registry import Registry
from pieapp.api.registries.models import SysRegistry
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.toolbars.mixins import ToolBarAccessorMixin
from pieapp.api.registries.toolbuttons.mixins import ToolButtonAccessorMixin

from metadata.widgets.albumpicker import AlbumCoverPicker


class ReadOnlyDelegate(QStyledItemDelegate):

    def create_editor(self, parent, option, index) -> None:
        return


class MetadataEditor(
    PiePlugin,
    ThemeAccessorMixin,
    ToolBarAccessorMixin,
    ToolButtonAccessorMixin,
):
    name = SysPlugin.MetadataEditor
    requires = [SysPlugin.Converter]

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg", scope=self.name)

    @on_plugin_ready(plugin=SysPlugin.Converter)
    def on_converter_available(self) -> None:
        self._snapshots = Registry(SysRegistry.Snapshots)
        self._converter = get_plugin(SysPlugin.Converter)
        self._converter.sig_table_item_added.connect(self._on_table_item_added)
        # self._converter.sig_on_snapshot_modified.connect(self._on_snapshot_modified)

        self._dialog = QDialog(self._parent)
        self._dialog.set_modal(True)
        self._dialog.set_object_name("MetadataEditor")
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.resize(*Global.DEFAULT_MIN_WINDOW_SIZE or (720, 450))

        self._main_grid_layout = QGridLayout()

        # Setup toolbar
        self._toolbar = self.add_toolbar(self._dialog, self.name)
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
            icon=self.get_svg_icon("icons/save.svg")
        )
        self._save_button.set_disabled(True)

        self._undo_button = self.add_tool_button(
            scope=self.name,
            name="undo",
            text=translate("Undo"),
            tooltip=translate("Undo"),
            icon=self.get_svg_icon("icons/undo.svg")
        )
        self._undo_button.set_disabled(True)

        self._redo_button = self.add_tool_button(
            scope=self.name,
            name="redo",
            text=translate("Redo"),
            tooltip=translate("Redo"),
            icon=self.get_svg_icon("icons/redo.svg")
        )
        self._redo_button.set_disabled(True)

        self.add_toolbar_item(self._toolbar.name, "save", self._save_button)
        self.add_toolbar_item(self._toolbar.name, "undo", self._undo_button)
        self.add_toolbar_item(self._toolbar.name, "redo", self._redo_button)
        self._toolbar.call()

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

        self._main_grid_layout.add_widget(self._toolbar, 0, 0, Qt.AlignmentFlag.AlignTop)
        self._main_grid_layout.add_widget(self._table_widget)

        self._dialog.set_layout(self._main_grid_layout)

    @Slot(MediaFile, int)
    def _on_table_item_added(self) -> None:
        self._converter.add_quick_action(
            name="edit",
            text=translate("Edit"),
            icon=self.get_plugin_icon(),
            callback=self._edit_file_button_connect,
            before="delete"
        )

    def _edit_file_button_connect(self, media_file_name: str) -> None:
        """
        -map 0:0 -map 1:0
        -c copy -id3v2_version 3
        -metadata:s:v title="album cover"
        -metadata:s:v comment="cover (front)" out.mp3
        """
        media_file: MediaFile = self._snapshots.get(media_file_name)
        self._dialog.set_window_title(f"{translate('Edit metadata')} - {media_file.info.filename}")

        self._save_button.clicked.connect(lambda: self._save_button_connect(media_file))
        self._undo_button.clicked.connect(lambda: self._undo_button_connect())
        self._redo_button.clicked.connect(lambda: self._redo_button_connect())

        contributors_list_widget = QListWidget()
        contributors_list_widget.add_items(media_file.metadata.additional_contributors)

        album_cover = media_file.metadata.album_cover
        album_cover_widget = AlbumCoverPicker(
            parent=self._dialog,
            image_path=album_cover.image_path.as_posix() if album_cover.image_path.exists() else None,
            picker_icon=self.get_svg_icon(
                key="icons/folder-open.svg",
                color=self.get_theme_property(ThemeProperties.AppIconColor)
            ),
            placeholder_text=translate("No image selected"),
            select_album_cover_text=translate("Select album cover image")
        )

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

        self._table_widget.set_item(0, 1, QTableWidgetItem(media_file.uuid))  # metadata.title
        self._table_widget.set_item(1, 1, QTableWidgetItem(media_file.metadata.genre))
        self._table_widget.set_item(2, 1, QTableWidgetItem(media_file.metadata.subgenre))
        self._table_widget.set_item(3, 1, QTableWidgetItem(media_file.metadata.track_number))
        self._table_widget.set_cell_widget(4, 1, album_cover_widget)
        self._table_widget.set_item(5, 1, QTableWidgetItem(media_file.metadata.primary_artist))
        self._table_widget.set_item(6, 1, QTableWidgetItem(media_file.metadata.publisher))
        self._table_widget.set_item(7, 1, QTableWidgetItem(media_file.metadata.explicit_content))
        self._table_widget.set_item(8, 1, QTableWidgetItem(media_file.metadata.lyrics_language))
        self._table_widget.set_item(9, 1, QTableWidgetItem(media_file.metadata.lyrics_publisher))
        self._table_widget.set_item(10, 1, QTableWidgetItem(media_file.metadata.composition_owner))
        self._table_widget.set_item(11, 1, QTableWidgetItem(media_file.metadata.release_language))
        self._table_widget.set_item(12, 1, QTableWidgetItem(media_file.metadata.featured_artist))
        self._table_widget.set_cell_widget(13, 1, contributors_list_widget)
        self._table_widget.set_item(14, 1, QTableWidgetItem(str(media_file.metadata.year_of_composition)))

        self._dialog.show()

    def _save_button_connect(self, media_file: MediaFile) -> None:
        pass

    def _undo_button_connect(self) -> None:
        pass

    def _redo_button_connect(self) -> None:
        pass


def main(parent: "QMainWindow", plugin_path: "Path"):
    return MetadataEditor(parent, plugin_path)

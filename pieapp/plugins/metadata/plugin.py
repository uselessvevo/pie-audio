from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem

from pieapp.api.globals import Global
from pieapp.api.managers.locales.helpers import translate
from pieapp.api.managers.shortcuts.mixins import ShortcutAccessorMixin
from pieapp.api.managers.themes.mixins import ThemeAccessorMixin
from pieapp.api.managers.toolbars.mixins import ToolBarAccessorMixin
from pieapp.api.managers.toolbuttons.mixins import ToolButtonAccessorMixin
from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.decorators import on_plugin_event
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.structs.media import MediaFile

from pieapp.api.structs.plugins import Plugin

from metadata.widgets.albumpicker import AlbumCoverPicker


class ReadOnlyDelegate(QStyledItemDelegate):

    def create_editor(self, parent, option, index) -> None:
        return


class MetadataEditor(
    PiePlugin,
    ThemeAccessorMixin,
    ToolBarAccessorMixin,
    ToolButtonAccessorMixin,
    ShortcutAccessorMixin
):
    name = Plugin.MetadataEditor
    requires = [Plugin.Converter]

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg", section=self.name)

    @on_plugin_event(target=Plugin.Converter)
    def on_converter_available(self) -> None:
        self._dialog = QDialog(self._parent)
        self._dialog.set_modal(True)
        self._dialog.set_object_name("MetadataEditor")
        self._dialog.set_window_title(translate("Edit metadata"))
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.resize(*Global.DEFAULT_MIN_WINDOW_SIZE or (720, 450))

        self._main_grid_layout = QGridLayout()

        # Setup toolbar
        self._toolbar = self.add_toolbar(self._dialog, self.name)
        self._toolbar.set_fixed_height(50)
        self._toolbar.set_contents_margins(6, 0, 10, 0)
        self._toolbar.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self._toolbar.set_object_name("MetadataToolBar")

        self._save_button = self.add_tool_button(
            section=self.name,
            name="save",
            text=translate("Save"),
            tooltip=translate("Save"),
            icon=self.get_svg_icon("icons/save.svg")
        )
        self._save_button.set_disabled(True)

        self._undo_button = self.add_tool_button(
            section=self.name,
            name="undo",
            text=translate("Undo"),
            tooltip=translate("Undo"),
            icon=self.get_svg_icon("icons/undo.svg")
        )
        self._undo_button.set_disabled(True)

        self._redo_button = self.add_tool_button(
            section=self.name,
            name="redo",
            text=translate("Redo"),
            tooltip=translate("Redo"),
            icon=self.get_svg_icon("icons/redo.svg")
        )
        self._redo_button.set_disabled(True)

        self.add_toolbar_item(self._toolbar.name, "save", self._save_button)
        self.add_toolbar_item(self._toolbar.name, "undo", self._undo_button)
        self.add_toolbar_item(self._toolbar.name, "redo", self._redo_button)

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

    @on_plugin_event(target=Plugin.Converter, event="converter_table_ready")
    def _on_converter_table_ready(self) -> None:
        """
        Add button into quick action menu
        """
        self._converter = get_plugin(Plugin.Converter)
        self._converter.add_quick_action(
            name="edit",
            text=translate("Edit"),
            icon=self.get_plugin_icon(),
            callback=self._edit_file_button_connect,
            before="delete"
        )

    def _edit_file_button_connect(self, media_file: MediaFile) -> None:
        """
        -map 0:0 -map 1:0
        -c copy -id3v2_version 3
        -metadata:s:v title="album cover"
        -metadata:s:v comment="cover (front)" out.mp3
        """
        self._save_button.clicked.connect(lambda: self._save_button_connect(media_file))
        self._undo_button.clicked.connect(lambda: self._undo_button_connect(media_file))
        self._redo_button.clicked.connect(lambda: self._redo_button_connect(media_file))

        contributors_list_widget = QListWidget()
        contributors_list_widget.add_items(media_file.metadata.additional_contributors)

        album_cover = media_file.metadata.album_cover

        album_cover_widget = AlbumCoverPicker(
            parent=self._dialog,
            image_path=album_cover.image_path.as_posix() if album_cover.image_path.exists() else None,
            picker_icon=self.get_svg_icon("icons/folder-open.svg", color="#f5d97f"),
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

        self._table_widget.set_item(0, 1, QTableWidgetItem(media_file.metadata.title))
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

    def _undo_button_connect(self, media_file: MediaFile) -> None:
        pass

    def _redo_button_connect(self, media_file: MediaFile) -> None:
        pass


def main(parent: "QMainWindow", plugin_path: "Path"):
    return MetadataEditor(parent, plugin_path)

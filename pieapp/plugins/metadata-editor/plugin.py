from PySide6.QtGui import Qt
from __feature__ import snake_case

from PySide6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QItemDelegate, QStyledItemDelegate, QGridLayout

from typing import Union

from pieapp.structs.media import MediaFile

from pieapp.structs.plugins import Plugin
from piekit.globals.loader import Global
from piekit.plugins.plugins import PiePlugin
from piekit.plugins.utils import get_plugin
from piekit.managers.icons.mixins import IconAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.managers.plugins.decorators import on_plugin_event


class ReadOnlyDelegate(QStyledItemDelegate):

    def create_editor(self, parent, option, index) -> None:
        return


class MetadataEditor(
    PiePlugin, LocalesAccessorMixin, IconAccessorMixin
):
    name = Plugin.MetadataEditor
    requires = [Plugin.Converter]

    @on_plugin_event(target=Plugin.Converter)
    def on_converter_available(self) -> None:
        self._dialog = QDialog(self._parent)
        self._dialog.set_window_title(self.get_translation("Edit metadata"))
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.resize(*Global.DEFAULT_MIN_WINDOW_SIZE or (720, 480))

        self._main_grid_layout = QGridLayout()
        self._table_widget = QTableWidget()
        self._table_widget.set_item_delegate_for_column(0, ReadOnlyDelegate(self._dialog))
        self._table_widget.set_column_count(2)
        self._main_grid_layout.add_widget(self._table_widget)

        self._dialog.set_layout(self._main_grid_layout)

    @on_plugin_event(target=Plugin.Converter, event="converter_table_ready")
    def on_converter_table_ready(self) -> None:
        self._converter = get_plugin(Plugin.Converter)
        self._converter.add_quick_action(
            name="edit",
            text=self.get_translation("Edit"),
            icon=self.get_svg_icon("edit.svg"),
            callback=self._edit_file_button_connect,
            before="delete"
        )

    def _edit_file_button_connect(self, media_file: MediaFile) -> None:
        self._dialog.show()

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon("app.svg", section=self.name)


def main(parent: "QMainWindow", plugin_path: "Path") -> Union[PiePlugin, None]:
    return MetadataEditor(parent, plugin_path)

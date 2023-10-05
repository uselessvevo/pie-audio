from __feature__ import snake_case

from PySide6.QtWidgets import QDialog

from typing import Union

from pieapp.structs.media import MediaFile

from pieapp.structs.plugins import Plugin
from piekit.globals.loader import Global
from piekit.plugins.plugins import PiePlugin
from piekit.plugins.utils import get_plugin
from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.managers.plugins.decorators import on_plugin_event


class MetadataEditor(
    PiePlugin, LocalesAccessorMixin, AssetsAccessorMixin
):
    name = Plugin.MetadataEditor
    requires = [Plugin.Converter]

    @on_plugin_event(target=Plugin.Converter)
    def on_converter_available(self) -> None:
        self._dialog = QDialog(self._parent)
        self._dialog.set_window_title(self.get_translation("About"))
        self._dialog.set_window_icon(self.get_plugin_svg_icon())
        self._dialog.resize(*Global.DEFAULT_MIN_WINDOW_SIZE or (720, 480))

    def call(self) -> None:
        self._dialog.show()

    @on_plugin_event(target=Plugin.Converter, event="converter_table_ready")
    def on_converter_table_ready(self) -> None:
        self._converter = get_plugin(Plugin.Converter)
        self._converter.add_side_menu_item(
            name="edit",
            text=self.get_translation("Edit"),
            icon=self.get_svg_icon("edit.svg"),
            callback=self._edit_file_button_connect,
            before="delete"
        )

    def _edit_file_button_connect(self, model: MediaFile) -> None:
        self._dialog.show()


def main(parent: "QMainWindow", plugin_path: "Path") -> Union[PiePlugin, None]:
    return MetadataEditor(parent, plugin_path)

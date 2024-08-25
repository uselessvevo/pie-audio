from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QGridLayout, QDialogButtonBox

from pieapp.api.converter.models import MediaFile
from pieapp.api.gloader import Global
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.snapshots.manager import Snapshots
from pieapp.widgets.buttons import Button, ButtonRole


class MediaPlugin(PiePlugin):
    # List of allowed file formats
    file_formats: list[str] = []
    target_plugin: str = SysPlugin.Converter

    @on_plugin_available(plugin=target_plugin)
    def _on_target_plugin_available(self) -> None:
        # SnapshotRegistry reference
        self._converter = get_plugin(SysPlugin.Converter)
        self._converter.sig_table_item_added.connect(self._on_table_item_added)

        # Define main dialog window
        self._dialog = QDialog(self._parent)
        self._dialog.set_window_flag(Qt.WindowType.WindowCloseButtonHint)
        self._dialog.set_object_name(self.name.capitalize())
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.resize(*Global.DEFAULT_MIN_WINDOW_SIZE)

        # Define main layout and button box
        self._main_layout = QGridLayout()
        self._button_box = QDialogButtonBox()

        self._ok_button = Button(ButtonRole.Primary)
        self._ok_button.set_text(translate("Ok"))

        self._cancel_button = Button()
        self._cancel_button.set_text(translate("Cancel"))

        self.on_target_plugin_available()

    def ok_button_connect(self, snapshot_name: str) -> None:
        Snapshots.sync_global_to_inner()
        Snapshots.restore_local_snapshots(snapshot_name)

    def cancel_button_connect(self, snapshot_name: str) -> None:
        Snapshots.restore_local_snapshots(snapshot_name)
        self.close()

    def connect_buttons(self) -> None:
        self._ok_button.clicked.connect(self.ok_button_connect)
        self._cancel_button.clicked.connect(self.cancel_button_connect)

    @Slot(MediaFile, int)
    def on_table_item_added(self, media_file: MediaFile, index: int) -> None:
        raise NotImplementedError(f"Method {__qualname__} must be implemented")

    def on_target_plugin_available(self) -> None:
        pass

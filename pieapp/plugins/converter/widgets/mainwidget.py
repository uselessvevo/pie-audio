from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout, QListWidgetItem

from pieapp.app.globals import AUDIO_EXTENSIONS
from pieapp.api.converter.models import MediaFile
from pieapp.api.globals import Global
from pieapp.api.models.themes import ThemeProperties, IconName
from pieapp.api.models.toolbars import ToolBarItem
from pieapp.api.plugins.mixins import CoreAccessorsMixin, WidgetsAccessorMixins
from pieapp.api.plugins.widgets import PiePluginWidget
from pieapp.api.registries.locales.helpers import translate
from pieapp.widgets.waitingspinner import create_wait_spinner

from converter.models import ConverterThemeProperties
from converter.widgets.item import ConverterItem
from converter.widgets.list import ConverterListWidget
from converter.widgets.search import ConverterSearch


class ConverterPluginWidget(PiePluginWidget, CoreAccessorsMixin, WidgetsAccessorMixins):
    name = ""
    dialog_type = None

    # Emit on converter table item added to list
    sig_table_item_added = Signal(MediaFile, int)

    # Emit on snapshot created
    sig_snapshot_created = Signal(MediaFile)

    # Emit on snapshot deleted
    sig_snapshot_deleted = Signal(MediaFile)

    # Emit on snapshot modified
    sig_snapshot_modified = Signal(MediaFile)

    # Emit on global snapshot restored
    sig_snapshot_restored = Signal()

    # Snapshot event methods

    def on_snapshot_created(self, state: bool):
        self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(state)

    def on_snapshot_modified(self, state: bool):
        self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(state)

    def on_snapshot_deleted(self, state: bool):
        self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(state)

    def on_snapshot_restored(self, state: bool):
        self.get_tool_button(self.name, ToolBarItem.Convert).set_enabled(state)
from PySide6.QtGui import QIcon

from pieapp.api.models.themes import IconName, ThemeProperties
from pieapp.api.plugins.quickaction import QuickAction
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.snapshots.registry import SnapshotRegistry
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin


class DeleteQuickAction(QuickAction, ThemeAccessorMixin):
    name = "delete"

    def get_tooltip(self) -> str:
        return translate("Delete")

    def get_icon(self) -> QIcon:
        return self.get_svg_icon(IconName.Delete, prop=ThemeProperties.ErrorColor)

    def on_click(self) -> None:
        SnapshotRegistry.remove(self._media_file_name)

from PySide6.QtGui import QIcon

from pieapp.api.globals import Global
from pieapp.api.models.themes import IconName
from pieapp.api.plugins.quickaction import QuickAction
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.snapshots.registry import SnapshotRegistry
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin


class EditQuickAction(QuickAction, ThemeAccessorMixin):
    name = "edit"

    def get_tooltip(self) -> str:
        return translate("Edit")

    def get_icon(self) -> QIcon:
        return self.get_svg_icon(IconName.App, self._plugin_name)

    def on_click(self) -> None:
        self.plugin_call_method(self.get_media_file_name())

    def get_enabled(self) -> tuple[bool, str]:
        media_file = SnapshotRegistry.get(self._media_file_name)
        if media_file is None:
            return False, f"{translate('Cant find this snapshot')}: {self._media_file_name}"

        in_list = media_file.info.file_format.lower() in Global.METADATA_EDITOR_ALLOWED_FILE_FORMATS
        if in_list is False:
            return False, translate("Plugin doesn't support this file format")

        return in_list, ""

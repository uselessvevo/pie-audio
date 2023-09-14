from typing import Any, Union

from PySide6.QtGui import QIcon

from piekit.config import Global
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager, Section


class AssetsAccessorMixin:
    """
    Config mixin
    """

    def get_asset(
        self,
        key: Any,
        default: Any = None,
        section: Union[str, Section] = Section.Shared
    ) -> Any:
        return Managers(SysManager.Assets).get(section or self.section, key, default)

    def get_asset_icon(
        self,
        key: Any,
        default: Any = None,
        section: Union[str, Section] = Section.Shared
    ):
        return QIcon(Managers(SysManager.Assets).get(section or self.section, key, default))

    def get_plugin_icon(self) -> "QIcon":
        return QIcon(Managers(SysManager.Assets).get(self.name, Global.PLUGIN_ICON_NAME))

    getAsset = get_asset
    getAssetIcon = get_asset_icon
    getPluginIcon = get_plugin_icon

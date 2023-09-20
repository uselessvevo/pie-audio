from typing import Any, Union

from PySide6.QtGui import QIcon

from piekit.globals import Global
from piekit.managers.registry import Managers
from piekit.managers.assets.utils import get_svg_icon
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
    ) -> QIcon:
        return QIcon(Managers(SysManager.Assets).get(section or self.section, key, default))

    def get_svg_icon(
        self,
        key: Any,
        color: str = "#dbdbdb",
        default: Any = None,
        section: Union[str, Section] = Section.Shared
    ) -> QIcon:
        return get_svg_icon(Managers(SysManager.Assets).get(section or self.section, key, default), color)

    def get_plugin_icon(self) -> "QIcon":
        return QIcon(Managers(SysManager.Assets).get(self.name, f"{Global.PLUGIN_ICON_NAME}.png"))

    def get_plugin_svg_icon(self, color: str = "#dbdbdb") -> "QIcon":
        return get_svg_icon(Managers(SysManager.Assets).get(self.name, f"{Global.PLUGIN_ICON_NAME}.svg"), color)

    getAsset = get_asset
    getAssetIcon = get_asset_icon
    getPluginIcon = get_plugin_icon

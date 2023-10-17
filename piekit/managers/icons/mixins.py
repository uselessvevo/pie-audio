from typing import Any, Union

from PySide6.QtGui import QIcon

from piekit.managers.registry import Managers
from piekit.managers.icons.utils import as_svg
from piekit.managers.structs import SysManager, Section


class IconAccessorMixin:
    """
    Config mixin
    """

    def get_icon_path(
        self,
        key: Any,
        default: Any = None,
        section: Union[str, Section] = Section.Shared
    ) -> Any:
        return Managers(SysManager.Icons).get(section or self.section, key, default)

    def get_icon(
        self,
        key: Any,
        default: Any = None,
        section: Union[str, Section] = Section.Shared
    ) -> QIcon:
        return QIcon(Managers(SysManager.Icons).get(section or self.section, key, default))

    def get_svg_icon(
        self,
        key: Any,
        color: str = "#dbdbdb",
        default: Any = None,
        section: Union[str, Section] = Section.Shared
    ) -> QIcon:
        icon_path = Managers(SysManager.Icons).get(section or self.section, key, default)
        return as_svg(icon_path, color)

    getAsset = get_icon_path
    getAssetIcon = get_icon

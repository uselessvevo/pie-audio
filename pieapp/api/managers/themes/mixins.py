from typing import Any, Union

from PySide6.QtGui import QIcon

from pieapp.api.managers.structs import Section
from pieapp.api.managers.structs import SysManager
from pieapp.api.managers.registry import Managers
from pieapp.api.managers.themes.helpers import as_svg


class ThemeAccessorMixin:
    """
    ThemeManager mixins
    """

    def get_file_path(
        self,
        key: Any,
        default: Any = None,
        section: Union[str, Section] = Section.Shared
    ) -> Any:
        return Managers(SysManager.Themes).get(section or self.section, key, default)

    def get_icon(
        self,
        key: Any,
        default: Any = None,
        section: Union[str, Section] = Section.Shared
    ) -> QIcon:
        return QIcon(Managers(SysManager.Themes).get(section or self.section, key, default))

    def get_svg_icon(
        self,
        key: Any,
        color: str = "#dbdbdb",
        default: Any = None,
        section: Union[str, Section] = Section.Shared
    ) -> QIcon:
        icon_path = Managers(SysManager.Themes).get(section or self.section, key, default)
        return as_svg(icon_path, color)

    def get_themes(self) -> list[str]:
        return Managers(SysManager.Themes).get_themes()

    def get_theme_property(self, prop_name: str, default: Any = None) -> Any:
        return Managers(SysManager.Themes).get_theme_property(prop_name, default)

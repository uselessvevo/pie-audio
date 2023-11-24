from typing import Any, Union

from PySide6.QtGui import QIcon

from piekit.managers.registry import Managers
from piekit.managers.themes.utils import as_svg
from piekit.managers.structs import SysManager, Section


class ThemeAccessorMixin:
    """
    Config mixin
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

    def get_theme_property(self, prop_name: str, default: Any = None) -> str:
        return Managers(SysManager.Themes).get_theme_property(prop_name, default)

    getIcon = get_icon
    getSvgIcon = get_svg_icon
    getFilePath = get_file_path
    getThemes = get_themes
    getThemeProperty = get_theme_property

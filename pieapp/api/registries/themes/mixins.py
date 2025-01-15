from typing import Any, Union

from PySide6.QtGui import QIcon

from pieapp.api.models.scopes import Scope
from pieapp.api.registries.themes.helpers import as_svg
from pieapp.api.registries.themes.registry import ThemeRegistry


class ThemeAccessorMixin:
    """
    ThemeManager mixins
    """

    def get_file_path(
        self,
        key: Any,
        default: Any = None,
        scope: str = Scope.Shared
    ) -> Any:
        return ThemeRegistry.get(scope or self.scope, key, default)

    def get_icon(
        self,
        key: Any,
        default: Any = None,
        scope: str = Scope.Shared
    ) -> QIcon:
        return QIcon(ThemeRegistry.get(scope or self.scope, key, default))

    def get_svg_icon(
        self,
        key: Any,
        scope: str = Scope.Shared,
        color: str = None,
        prop: str = None,
        default: Any = None
    ) -> QIcon:
        if prop:
            color = self.get_theme_property(prop)
        icon_path = ThemeRegistry.get(scope or self.scope, key, default)
        return as_svg(icon_path, color)

    @staticmethod
    def get_themes() -> list[str]:
        return ThemeRegistry.get_themes()

    @staticmethod
    def get_theme_property(prop_name: str, default: Any = None) -> Any:
        return ThemeRegistry.get_theme_property(prop_name, default)

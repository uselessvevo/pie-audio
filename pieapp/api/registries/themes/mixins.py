from typing import Any, Union

from PySide6.QtGui import QIcon

from pieapp.api.registries.models import Scope
from pieapp.api.registries.themes.helpers import as_svg
from pieapp.api.registries.themes.manager import Themes


class ThemeAccessorMixin:
    """
    ThemeManager mixins
    """

    def get_file_path(
        self,
        key: Any,
        default: Any = None,
        scope: Union[str, Scope] = Scope.Shared
    ) -> Any:
        return Themes.get(scope or self.scope, key, default)

    def get_icon(
        self,
        key: Any,
        default: Any = None,
        scope: Union[str, Scope] = Scope.Shared
    ) -> QIcon:
        return QIcon(Themes.get(scope or self.scope, key, default))

    def get_svg_icon(
        self,
        key: Any,
        color: str = None,
        prop: str = None,
        default: Any = None,
        scope: Union[str, Scope] = Scope.Shared
    ) -> QIcon:
        if prop:
            color = self.get_theme_property(prop)
        icon_path = Themes.get(scope or self.scope, key, default)
        return as_svg(icon_path, color)

    def get_themes(self) -> list[str]:
        return Themes.get_themes()

    def get_theme_property(self, prop_name: str, default: Any = None) -> Any:
        return Themes.get_theme_property(prop_name, default)

from typing import Any, Union

from PySide6.QtGui import QIcon

from pieapp.api.registries.models import Scope
from pieapp.api.registries.models import SysRegistry
from pieapp.api.registries.registry import Registry
from pieapp.api.registries.themes.helpers import as_svg


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
        return Registry(SysRegistry.Themes).get(scope or self.scope, key, default)

    def get_icon(
        self,
        key: Any,
        default: Any = None,
        scope: Union[str, Scope] = Scope.Shared
    ) -> QIcon:
        return QIcon(Registry(SysRegistry.Themes).get(scope or self.scope, key, default))

    def get_svg_icon(
        self,
        key: Any,
        color: str = None,
        default: Any = None,
        scope: Union[str, Scope] = Scope.Shared
    ) -> QIcon:
        icon_path = Registry(SysRegistry.Themes).get(scope or self.scope, key, default)
        return as_svg(icon_path, color)

    def get_themes(self) -> list[str]:
        return Registry(SysRegistry.Themes).get_themes()

    def get_theme_property(self, prop_name: str, default: Any = None) -> Any:
        return Registry(SysRegistry.Themes).get_theme_property(prop_name, default)

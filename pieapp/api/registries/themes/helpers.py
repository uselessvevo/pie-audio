from __feature__ import snake_case

from typing import Any, Union

from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon

from pieapp.api.registries.models import Scope
from pieapp.api.registries.themes.manager import Themes


def as_svg(file: str, color: Union[str, list] = None) -> QIcon:
    if not file:
        return QIcon()

    pixmap = QPixmap(file)
    painter = QPainter(pixmap)
    painter.set_composition_mode(QPainter.CompositionMode.CompositionMode_SourceIn)

    painter.fill_rect(pixmap.rect(), QColor.from_string(color))
    painter.end()

    return QIcon(pixmap)


def get_file_path(
    key: Any,
    default: Any = None,
    scope: Union[str, Scope] = Scope.Shared
) -> Any:
    return Themes.get(scope, key, default)


def get_icon(
    key: Any,
    default: Any = None,
    scope: Union[str, Scope] = Scope.Shared
) -> QIcon:
    return QIcon(Themes.get(scope, key, default))


def get_svg_icon(
    key: Any,
    color: str,
    default: Any = None,
    scope: Union[str, Scope] = Scope.Shared
) -> QIcon:
    icon_path = Themes.get(scope, key, default)
    return as_svg(icon_path, color)


def get_current_theme() -> str:
    return Themes.get_theme()


def get_themes() -> list[str]:
    return Themes.get_themes()


def get_theme_property(prop_name: str, default: Any = None) -> Any:
    return Themes.get_theme_property(prop_name, default)

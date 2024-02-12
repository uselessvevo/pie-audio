from __feature__ import snake_case

from typing import Any, Union

from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon

from pieapp.api.managers.registry import Managers
from pieapp.api.managers.structs import SysManager, Section


def as_svg(file: str, color: str) -> QIcon:
    if not file:
        return QIcon()

    pixmap = QPixmap(file)
    painter = QPainter(pixmap)
    painter.set_composition_mode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fill_rect(pixmap.rect(), QColor(color))
    painter.end()

    return QIcon(pixmap)


def get_file_path(
    key: Any,
    default: Any = None,
    section: Union[str, Section] = Section.Shared
) -> Any:
    return Managers(SysManager.Themes).get(section, key, default)


def get_icon(
    key: Any,
    default: Any = None,
    section: Union[str, Section] = Section.Shared
) -> QIcon:
    return QIcon(Managers(SysManager.Themes).get(section, key, default))


def get_svg_icon(
    key: Any,
    color: str = "#dbdbdb",
    default: Any = None,
    section: Union[str, Section] = Section.Shared
) -> QIcon:
    icon_path = Managers(SysManager.Themes).get(section, key, default)
    return as_svg(icon_path, color)


def get_themes() -> list[str]:
    return Managers(SysManager.Themes).get_themes()


def get_theme_property(prop_name: str, default: Any = None) -> Any:
    return Managers(SysManager.Themes).get_theme_property(prop_name, default)

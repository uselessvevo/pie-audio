from __feature__ import snake_case

import os
import importlib
import importlib.util
from pathlib import Path

from piekit.globals import Global
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon


def get_theme(theme_name: str) -> str:
    """
    Parse and get stylesheet
    """
    themes_root = Global.APP_ROOT / Global.ASSETS_FOLDER / 'themes'
    theme_name = themes_root / theme_name
    themes_list: list[Path] = list(i for i in themes_root.glob('*') if i.is_dir())
    stylesheet: str = ''

    # Check if folder exists
    if not theme_name.exists():
        # Get one of theme
        if themes_list and os.path.exists(themes_list[0]):
            theme_name = Path(f'assets/themes/{themes_list[0]}')
        else:
            theme_name = None

    if theme_name and theme_name.exists():
        stylesheet = (theme_name / "theme.qss").read_text(encoding="utf-8")

    return stylesheet


def get_palette(theme_name: str):
    """
    Get palette module from theme folder
    Args:
        theme_name (str): theme name
    Returns:
        palette (module): app.setPalette(palette.getPalette())
    """
    theme_folder = Global.APP_ROOT / Global.ASSETS_FOLDER / "themes" / theme_name

    if theme_folder.exists():
        spec = importlib.util.spec_from_file_location(
            name='palette',
            location=str(theme_folder / 'palette.py')
        )
        palette = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(palette)
        return palette.get_palette()


def as_svg(file: str, color: str = "#7cd162") -> QIcon:
    if not file:
        return QIcon()

    pixmap = QPixmap(file)
    painter = QPainter(pixmap)
    painter.set_composition_mode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fill_rect(pixmap.rect(), QColor(color))
    painter.end()

    return QIcon(pixmap)


# Qt aliases
getTheme = get_theme
getPalette = get_palette
getSvgIcon = as_svg

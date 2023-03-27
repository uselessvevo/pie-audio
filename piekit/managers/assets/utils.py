import os
import re
import importlib
import importlib.util
from pathlib import Path

from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon

from piekit.utils.files import read_json
from piekit.system.config import Config


def parse_stylesheet(path: str, keys: dict = None) -> str:
    if not os.path.exists(f'{path}/theme.qss'):
        with open(f'{path}/theme.template.qss', encoding='utf-8') as output:
            # Template pattern and variables
            pattern = r'((\@)([A-Za-z]+[\d]+[\w@]*|[A-Za-z]+[\w@]*))'
            variables = read_json(f'{path}/variables.json')
            variables.update(keys)

            # Template content
            stylesheet = output.read()
            matches = re.findall(pattern, stylesheet)

            for match in matches:
                stylesheet = stylesheet.replace(match[0], variables[match[2]])

        with open(f'{path}/theme.qss', 'w') as output:
            output.write(stylesheet)
    else:
        # Create empty theme file
        with open(f'{path}/theme.qss', encoding='utf-8') as output:
            stylesheet = output.read()

    return stylesheet


def get_theme(theme_name: str) -> str:
    """
    Parse and get stylesheet
    """
    themes_root = Config.APP_ROOT / Config.ASSETS_FOLDER / 'themes'
    theme_name = themes_root / theme_name
    themes_list: list[Path] = list(i for i in themes_root.glob('*') if i.is_dir())
    stylesheet: str = ''

    # Check if folder exists
    if not theme_name.exists():
        # Get one of theme
        if themes_list and os.path.exists(themes_list[0]):
            theme_name = f'assets/themes/{themes_list[0]}'
        else:
            theme_name = None

    if theme_name and theme_name.exists():
        stylesheet = parse_stylesheet(theme_name, {
            'themeFolder': str(theme_name.as_posix())
        })

    return stylesheet


def get_palette(theme_name: str):
    """
    Get palette module from theme folder
    Args:
        theme_name (str): theme name
    Returns:
        palette (module): app.setPalette(palette.getPalette())
    """
    theme_folder = Config.APP_ROOT / Config.ASSETS_FOLDER / "themes" / theme_name
    palette = None

    if theme_folder.exists():
        spec = importlib.util.spec_from_file_location(
            name='palette',
            location=str(theme_folder / 'palette.py')
        )
        palette = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(palette)
        return palette.getPalette()


def set_svg_color(file: str, color: str = "#7cd162"):
    pixmap = QPixmap(file)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()

    return QIcon(pixmap)


# Qt aliases
getTheme = get_theme
getPalette = get_palette
parseStylesheet = parse_stylesheet
setSvgColor = set_svg_color

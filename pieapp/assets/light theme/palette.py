from __feature__ import snake_case

from PySide6.QtGui import QPalette
from PySide6.QtGui import QColor


def get_palette():
    palette = QPalette()
    palette.set_color(QPalette.ColorRole.Link, QColor(0, 0, 0))
    palette.set_color(QPalette.ColorRole.LinkVisited, QColor(0, 0, 0))

    return palette

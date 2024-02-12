from PySide6.QtGui import QPalette
from PySide6.QtGui import QColor


def get_palette():
    palette = QPalette()
    palette.set_color(QPalette.ColorRole.Link, QColor(242, 242, 242))
    palette.set_color(QPalette.ColorRole.LinkVisited, QColor(242, 242, 242))

    return palette

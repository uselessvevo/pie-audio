from PySide6.QtGui import QPalette
from PySide6.QtGui import QColor


def getPalette():
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Link, QColor(242, 242, 242))
    palette.setColor(QPalette.ColorRole.LinkVisited, QColor(242, 242, 242))

    return palette

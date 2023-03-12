# fuck you qt
# this module was made
# because i can't set link (href) color in qss file
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor


def getPalette():
    palette = QPalette()
    palette.setColor(QPalette.Link, QColor(242, 242, 242))
    palette.setColor(QPalette.LinkVisited, QColor(242, 242, 242))

    return palette

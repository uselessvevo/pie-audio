from __feature__ import snake_case
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon


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
asSvg = as_svg

from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtGui import QPixmap, QImage, QPainter


def SplashScreen(path: str) -> QSplashScreen:
    """ Simple splash screen """
    splashImage = QImage(720, 480, QImage.Format_ARGB32_Premultiplied)
    splashImage.fill(0)

    svgPainter = QPainter(splashImage)
    svgRenderer = QSvgRenderer(path)
    svgRenderer.render(svgPainter)
    svgPainter.end()

    pixmap = QPixmap.fromImage(splashImage)
    pixmap = pixmap.copy(0, 0, 720, 480)

    splashScreen = QSplashScreen(pixmap)
    splashFont = splashScreen.font()
    splashFont.setPixelSize(14)
    splashScreen.setFont(splashFont)

    return splashScreen

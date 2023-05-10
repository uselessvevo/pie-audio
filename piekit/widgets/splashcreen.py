from PySide6.QtCore import QObject
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QLabel, QSplashScreen
from PySide6.QtGui import QPixmap, QImage, QPainter


class SplashScreen(QSplashScreen):

    def __init__(self, path: str = None) -> None:
        super().__init__()

        splashImage = QImage(720, 480, QImage.Format.Format_ARGB32_Premultiplied)
        splashImage.fill(0)

        svgPainter = QPainter(splashImage)
        svgRenderer = QSvgRenderer(path)
        svgRenderer.render(svgPainter)
        svgPainter.end()

        pixmap = QPixmap.fromImage(splashImage)
        pixmap = pixmap.copy(0, 0, 720, 480)

        self.splashScreen = QSplashScreen(pixmap)
        splashFont = self.splashScreen.font()
        splashFont.setPixelSize(14)
        self.splashScreen.setFont(splashFont)

        self.label = QLabel(self.splashScreen)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.setGeometry(50, 50, 50, 50)

    def setText(self, text: str) -> None:
        self.label.setText(text)

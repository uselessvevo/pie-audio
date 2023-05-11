from __feature__ import snake_case

from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QLabel, QSplashScreen
from PySide6.QtGui import QPixmap, QImage, QPainter


class SplashScreen(QSplashScreen):

    def __init__(self, path: str = None) -> None:
        super().__init__()

        splash_image = QImage(720, 480, QImage.Format.Format_ARGB32_Premultiplied)
        splash_image.fill(0)

        svg_painter = QPainter(splash_image)
        svg_renderer = QSvgRenderer(path)
        svg_renderer.render(svg_painter)
        svg_painter.end()

        pixmap = QPixmap.from_image(splash_image)
        pixmap = pixmap.copy(0, 0, 720, 480)

        self.splash_screen = QSplashScreen(pixmap)
        splash_font = self.splash_screen.font()
        splash_font.set_pixel_size(14)
        self.splash_screen.set_font(splash_font)

        self.label = QLabel(self.splash_screen)
        self.label.set_pixmap(pixmap)
        self.label.set_scaled_contents(True)
        self.set_geometry(50, 50, 50, 50)

    def set_text(self, text: str) -> None:
        self.label.set_text(text)

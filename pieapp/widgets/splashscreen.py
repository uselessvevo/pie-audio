from __feature__ import snake_case

from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QPixmap, QImage, QPainter


class SplashScreen(QSplashScreen):

    def __init__(self, image_path: str) -> None:
        super(SplashScreen, self).__init__()

        splash_image = QImage(720, 480, QImage.Format.Format_ARGB32_Premultiplied)
        splash_image.fill(0)

        svg_painter = QPainter(splash_image)
        svg_renderer = QSvgRenderer(image_path)
        svg_renderer.render(svg_painter)
        svg_painter.end()

        pixmap = QPixmap.from_image(splash_image)
        pixmap = pixmap.copy(0, 0, 720, 480)

        self.set_pixmap(pixmap)
        splash_font = self.font()
        splash_font.set_pixel_size(14)
        self.set_font(splash_font)

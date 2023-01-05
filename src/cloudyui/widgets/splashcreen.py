from PyQt5 import QtCore, QtSvg


def SplashScreen(path: str, **options) -> QtSvg.QSvgWidget:
    """ Create splash screen. Forked from Spyder: spyder/app/utils.py """
    with open(path, 'r') as svg_out:
        svg_data = svg_out.read().format(**options)
        svg_data = bytearray(svg_data, encoding='utf-8')

    splash = QtSvg.QSvgWidget()
    splash.renderer().load(svg_data)
    splash.setWindowFlags(QtCore.Qt.WindowFlags(
        QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
    ))
    splash.setFixedWidth(options.get('width', 720))
    splash.setFixedHeight(options.get('height', 480))

    return splash

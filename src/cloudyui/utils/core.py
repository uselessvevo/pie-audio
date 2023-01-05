import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt


def getApplication(*args, **kwargs):
    app = QtWidgets.QApplication.instance()
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    if app is None:
        if not args:
            args = ([''],)
        app = QtWidgets.QApplication(*args, **kwargs)
    return app


def restartApplication() -> None:
    QtCore.QCoreApplication.quit()
    QtCore.QProcess.startDetached(sys.executable, sys.argv)

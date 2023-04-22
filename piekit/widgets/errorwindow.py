import sys
from typing import Union

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QErrorMessage

from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QPushButton


def ErrorWindow(err_value: str, err_traceback: Union[tuple, list]):
    """
    A window will close after it initialization
    """
    app = QApplication.instance()
    app.setQuitOnLastWindowClosed(True)
    app.setWindowIcon(app.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning))

    error_message = f"An error has been occurred: {err_value}"
    err_traceback = "<br>".join(i for i in err_traceback)
    error_message = f"{error_message}<br>==========================<br>{err_traceback}"

    window = QErrorMessage()
    window.resize(600, 350)
    window.finished.connect(lambda e: app.quit)

    window.findChild(QLabel, "").setVisible(False)
    window.findChild(QCheckBox, "").setVisible(False)
    window.findChild(QPushButton, "").setVisible(False)
    window.setWindowTitle(f"Error: {err_value}")
    window.showMessage(error_message)

    sys.exit(app.exec())

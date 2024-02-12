from __feature__ import snake_case

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
    app.set_quit_on_last_window_closed(True)
    app.set_window_icon(app.style().standard_icon(QStyle.StandardPixmap.SP_MessageBoxWarning))

    error_message = f"An error has been occurred: {err_value}"
    err_traceback = "<br>".join(i for i in err_traceback)
    error_message = f"{error_message}<br><br>{err_traceback}"

    window = QErrorMessage()
    window.resize(600, 350)
    window.finished.connect(lambda _: app.quit)

    window.find_child(QLabel, "").set_visible(False)
    window.find_child(QCheckBox, "").set_visible(False)
    window.find_child(QPushButton, "").set_visible(False)
    window.set_window_title(f"Error: {err_value}")
    window.show_message(error_message)

    sys.exit(app.exec())

from __feature__ import snake_case

from typing import Union

from PySide6.QtWidgets import QMainWindow

from pieapp.api.utils.qapp import get_application


def get_main_window() -> Union[QMainWindow, None]:
    app = get_application().instance()
    for widget in app.top_level_widgets():
        if isinstance(widget, QMainWindow):
            return widget

    return None


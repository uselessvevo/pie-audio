from __feature__ import snake_case

import os
import sys
import traceback
from typing import Union

from PySide6.QtCore import QCoreApplication, QProcess
from PySide6.QtWidgets import QApplication, QMainWindow

from pieapp.widgets.errorwindow import ErrorWindow


def get_application(*args, **kwargs) -> QApplication:
    app = QApplication.instance()
    if app is None:
        if not args:
            args = ([''],)
        app = QApplication(*args, **kwargs)

    return app


def get_main_window() -> Union[QMainWindow, None]:
    app = QApplication.instance()
    for widget in app.top_level_widgets():
        if isinstance(widget, QMainWindow):
            return widget

    return None


def restart_application() -> None:
    from pieapp.api.gloader import Global
    from pieapp.api.plugins.registry import Plugins

    if not Global.IS_DEV_ENV or False:
        file_extension = "exe" if os.name == "nt" else ""
        sys.argv[0] = f"{sys.argv[0]}.{file_extension}"

    Plugins.shutdown_plugins(all_plugins=True)
    QCoreApplication.quit()
    QProcess.start_detached(sys.executable, sys.argv)


def except_hook(_, exc_value, exc_traceback):
    traceback_collect = []
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            traceback_collect.append(repr(line).replace("\\n", ""))

    ErrorWindow(exc_value, traceback_collect)

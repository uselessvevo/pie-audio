import sys
import traceback
from typing import Union

from __feature__ import snake_case
from PySide6.QtCore import QCoreApplication, QProcess
from PySide6.QtWidgets import QApplication, QMainWindow

from piekit.globals import Global
from piekit.managers.registry import Managers
from piekit.utils.files import write_json
from piekit.widgets.errorwindow import ErrorWindow


def get_application(*args, **kwargs):
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
    Managers.shutdown(full_house=True)
    QCoreApplication.quit()
    QProcess.start_detached(sys.executable, sys.argv)


def check_crabs() -> bool:
    return (
            Global.USER_ROOT.exists()
            or (Global.USER_ROOT / Global.CONFIGS_FOLDER).exists()
            or (Global.USER_ROOT / Global.CONFIGS_FOLDER / Global.CONFIG_FILE_NAME).exists()
    )


def restore_crabs() -> None:
    if not Global.USER_ROOT.exists():
        Global.USER_ROOT.mkdir()
        (Global.USER_ROOT / Global.USER_CONFIG_FOLDER).mkdir()
        (Global.USER_ROOT / Global.USER_PLUGINS_FOLDER).mkdir()
        write_json(
            file=str(Global.USER_ROOT / Global.USER_CONFIG_FOLDER / Global.CONFIG_FILE_NAME),
            data={"crab_status": "what a crab doin?"},
            create=True
        )


def except_hook(_, exc_value, exc_traceback):
    traceback_collect = []
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            traceback_collect.append(repr(line).replace("\\n", ""))

    ErrorWindow(exc_value, traceback_collect)


restartApplication = restart_application
getApplication = get_application
checkCrabs = check_crabs

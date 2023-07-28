import sys
import traceback
from typing import Union

from __feature__ import snake_case
from PySide6.QtCore import QCoreApplication, QProcess
from PySide6.QtWidgets import QApplication, QMainWindow

from piekit.config import Config
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
        Config.USER_ROOT.exists()
        or (Config.USER_ROOT / Config.CONFIGS_FOLDER).exists()
        or (Config.USER_ROOT / Config.CONFIGS_FOLDER / Config.CONFIG_FILE_NAME).exists()
    )


def restore_crabs() -> None:
    if not Config.USER_ROOT.exists():
        Config.USER_ROOT.mkdir()
        (Config.USER_ROOT / Config.USER_CONFIG_FOLDER).mkdir()
        (Config.USER_ROOT / Config.USER_PLUGINS_FOLDER).mkdir()
        write_json(
            file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / Config.CONFIG_FILE_NAME),
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

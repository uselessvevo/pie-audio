import sys
import traceback

from PyQt5 import QtWidgets, QtCore
from PyQt6.QtCore import Qt

from piekit.system import Config
from piekit.managers.registry import Managers
from piekit.widgets.errorwindow import ErrorWindow


def get_application(*args, **kwargs):
    app = QtWidgets.QApplication.instance()
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    if app is None:
        if not args:
            args = ([''],)
        app = QtWidgets.QApplication(*args, **kwargs)
    return app


def restart_application() -> None:
    Managers.unmount(full_house=True)
    QtCore.QCoreApplication.quit()
    QtCore.QProcess.startDetached(sys.executable, sys.argv)


def check_crabs() -> bool:
    if not Config.USER_ROOT.exists():
        return False

    user_folder = Config.USER_ROOT / Config.CONFIGS_FOLDER
    req_files = set((Config.SYSTEM_ROOT / i).name for i in Config.TEMPLATE_FILES)
    ex_files = set(i.name for i in user_folder.rglob("*.json"))
    return req_files == ex_files


def restore_crabs() -> None:
    if not Config.USER_ROOT.exists():
        Config.USER_ROOT.mkdir()
        (Config.USER_ROOT / Config.USER_CONFIG_FOLDER).mkdir()
        (Config.USER_ROOT / Config.USER_PLUGINS_FOLDER).mkdir()


def except_hook(exc_type, exc_value, exc_traceback):
    traceback_collect = []
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            traceback_collect.append(repr(line).replace("\\n", ""))

    ErrorWindow(exc_type, exc_value, traceback_collect)


restartApplication = restart_application
getApplication = get_application
checkCrabs = check_crabs

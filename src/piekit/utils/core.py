import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

from piekit.managers.registry import Managers
from piekit.system.loader import Config


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
    user_folder = Config.USER_ROOT / Config.CONFIGS_FOLDER
    templates_folder = Config.SYSTEM_ROOT / Config.TEMPLATE_FOLDER
    req_files = set(i.name for i in templates_folder.rglob("*.json"))
    ex_files = set(i.name for i in user_folder.rglob("*.json"))
    return req_files == ex_files


restartApplication = restart_application
getApplication = get_application
checkCrabs = check_crabs

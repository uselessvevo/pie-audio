import os
import sys
import traceback

from cloudykit.system.manager import System
from cloudykit.utils.files import read_json
from cloudykit.utils.modules import import_by_string
from cloudyui.base.errorbox import SystemErrorWindow


def except_hook(exc_type, exc_value, exc_traceback):
    traceback_collect = []
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            traceback_collect.append(repr(line).replace('\\n', ''))

    SystemErrorWindow(exc_type, exc_value, traceback_collect)


def setup_system_manager(root: str) -> None:
    System.mount(root)
    managers = read_json(System.root / 'configs/cloudykit.json')
    managers = managers.get('managers')

    if not managers:
        raise RuntimeError('No managers were found')

    System.registry.mount(*managers)


def get_qt_app(*args, **kwargs):
    from PyQt5 import QtWidgets
    from PyQt5.QtCore import Qt

    app = QtWidgets.QApplication.instance()
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    if app is None:
        if not args:
            args = ([''],)
        app = QtWidgets.QApplication(*args, **kwargs)
    return app


def main():
    setup_system_manager(os.path.dirname(__file__))
    # sys.excepthook = except_hook
    import_by_string(System.config.get('cloudykit.entrypoint'))()


if __name__ == '__main__':
    main()

import os
from pathlib import Path

from cloudykit.system.manager import System
from cloudykit.utils.files import read_json
from cloudykit.utils.modules import import_by_string


def setup_system_manager(root: str) -> None:

    System.mount(root)
    managers = read_json(System.root / 'configs/cloudykit.json')
    managers = managers.get('managers')

    System.managers.mount(*managers)


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
    import_by_string(System.config.get('cloudykit.entrypoint'))()


if __name__ == '__main__':
    main()

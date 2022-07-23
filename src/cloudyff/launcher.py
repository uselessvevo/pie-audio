import os
import sys
import traceback

from cloudykit.managers.system.manager import System
from cloudykit.utils.files import read_json
from cloudykit.utils.modules import import_by_string
from cloudyui.base.errorbox import SystemErrorWindow
from cloudyui.utils.qt import getQtApp


def except_hook(exc_type, exc_value, exc_traceback):
    traceback_collect = []
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            traceback_collect.append(repr(line).replace('\\n', ''))

    SystemErrorWindow(exc_type, exc_value, traceback_collect)


def check_user_crabs() -> bool:
    if System.user_root.exists():
        if not all((System.user_root / i).exists() for i in ('assets.json', 'locales.json')):
            return False


def setup_managers(root: str) -> None:
    System.mount(root)
    config = read_json(System.root / 'configs/cloudykit.json')
    managers = config.get('managers')

    if not managers:
        raise RuntimeError('No managers were found')

    System.registry.mount(*managers)

    if not check_user_crabs():
        app = getQtApp()
        from wizard import SetupWizard

        wizard = SetupWizard()
        wizard.show()
        sys.exit(app.exec_())


def main():
    setup_managers(os.path.dirname(__file__))
    sys.excepthook = except_hook
    import_by_string(System.config.get('cloudykit.entrypoint'))()


if __name__ == '__main__':
    main()

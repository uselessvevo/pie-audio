import sys
import traceback
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from piekit.managers.registry import Managers
from piekit.system.loader import Config
from piekit.utils.modules import is_debug
from piekit.utils.modules import import_by_string
from piekit.utils.core import check_crabs

from piekit.utils.core import getApplication
from piekit.widgets.splashcreen import SplashScreen
from piekit.widgets.errorwindow import ErrorWindow


def except_hook(exc_type, exc_value, exc_traceback):
    traceback_collect = []
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            traceback_collect.append(repr(line).replace("\\n", ""))

    ErrorWindow(exc_type, exc_value, traceback_collect)


def setup_application() -> None:
    splash = None
    app = getApplication(sys.argv)

    if not is_debug() and Path("branding/splash.svg").exists():
        splash = SplashScreen(
            path="branding/splash.svg",
            width=720,
            height=480,
            project_name="CloudyFF"
        )
        splash.show()

    QApplication.processEvents()
    Managers.mount(*Config.MANAGERS)

    if not check_crabs():
        if splash:
            splash.close()

        from wizard import SetupWizard

        wizard = SetupWizard()
        wizard.show()
        sys.exit(app.exec_())

    if splash:
        splash.close()


def main():
    sys.excepthook = except_hook
    setup_application()
    import_by_string(Config.PIEAPP_ENTRYPOINT)()


if __name__ == "__main__":
    main()

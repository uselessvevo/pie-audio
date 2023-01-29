import os
import sys
import traceback
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from cloudykit.system.manager import System
from cloudykit.utils.modules import is_debug
from cloudykit.utils.modules import import_by_string
from cloudykit.utils.system import check_crabs

from cloudykit.utils.core import getApplication
from cloudyui.widgets.splashcreen import SplashScreen
from cloudyui.widgets.errorwindow import ErrorWindow


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
    System.mount()

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
    # sys.excepthook = except_hook
    setup_application()
    import_by_string(os.getenv("CLOUDYAPP_ENTRYPOINT", "main.main"))()


if __name__ == "__main__":
    main()

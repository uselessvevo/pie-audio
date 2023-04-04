import os
import sys
from PySide6.QtWidgets import QApplication

from piekit.system import Config
from piekit.system.types import EDict, EList
from pieapp.wizard.wizard import SetupWizard
from piekit.managers.registry import Managers
from piekit.utils.modules import is_debug
from piekit.utils.core import check_crabs, except_hook
from piekit.utils.core import restore_crabs
from piekit.utils.core import get_application
from piekit.widgets.splashcreen import SplashScreen


def setup_application() -> None:
    sys.excepthook = except_hook

    Config.add_type(EList)
    Config.add_type(EDict)
    Config.load_module("piekit.system.config", False)
    Config.load_module(os.environ.get("CONFIG_MODULE_NAME", "pieapp.config"))

    splash = None
    app = get_application(sys.argv)
    splash_image = Config.APP_ROOT / Config.ASSETS_FOLDER / "splash.svg"

    if not is_debug() and splash_image.exists():
        splash = SplashScreen(str(splash_image))
        splash.show()

    QApplication.processEvents()

    if not check_crabs():
        restore_crabs()
        Managers.mount(*Config.MANAGERS)

        if splash:
            splash.close()

        wizard = SetupWizard()
        wizard.show()
        sys.exit(app.exec())

    Managers.mount(*Config.MANAGERS)

    if splash:
        splash.close()

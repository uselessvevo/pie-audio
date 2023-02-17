import sys
from PyQt5.QtWidgets import QApplication

from pieapp.wizard.wizard import SetupWizard
from piekit.managers.registry import Managers
from piekit.system.loader import Config
from piekit.utils.modules import is_debug
from piekit.utils.core import check_crabs
from piekit.utils.core import restore_crabs
from piekit.utils.core import get_application
from piekit.widgets.splashcreen import SplashScreen


def setup_application() -> None:
    splash = None
    app = get_application(sys.argv)
    splash_image = Config.APP_ROOT / Config.ASSETS_FOLDER / "splash.svg"

    if not is_debug() and splash_image.exists():
        splash = SplashScreen(str(splash_image))
        splash.show()

    QApplication.processEvents()
    Managers.mount(*Config.MANAGERS)

    if not check_crabs():
        restore_crabs()

        if splash:
            splash.close()

        wizard = SetupWizard()
        wizard.show()
        sys.exit(app.exec_())

    if splash:
        splash.close()

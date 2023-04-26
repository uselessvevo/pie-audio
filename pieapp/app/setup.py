import os
import sys

from piekit.config import Config, Lock
from pieapp.wizard.wizard import SetupWizard
from piekit.managers.registry import Managers
from piekit.utils.modules import is_debug
from piekit.utils.core import check_crabs
from piekit.utils.core import except_hook
from piekit.utils.core import restore_crabs
from piekit.utils.core import get_application
from piekit.widgets.splashcreen import SplashScreen


def setup_application() -> None:
    sys.excepthook = except_hook

    Config.add_handlers(Lock)
    Config.import_module(os.getenv("PIE_SYS_CONFIG_MODULE", "piekit.config.config"))
    Config.import_module(os.getenv("PIE_APP_CONFIG_MODULE", "pieapp.config"))

    splash = None
    app = get_application(sys.argv)
    splash_image = Config.APP_ROOT / Config.ASSETS_FOLDER / "splash.svg"

    if not is_debug() and splash_image.exists():
        splash = SplashScreen(str(splash_image))
        splash.show()

    app.processEvents()

    if not check_crabs():
        restore_crabs()
        for manager in Config.INITIAL_MANAGERS:
            Managers.from_config(manager)

        if splash:
            splash.close()

        wizard = SetupWizard()
        wizard.show()
        sys.exit(app.exec())

    for manager in Config.MANAGERS:
        Managers.from_config(manager)

    if splash:
        splash.close()

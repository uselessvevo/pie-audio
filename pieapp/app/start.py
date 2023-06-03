import PySide6
from __feature__ import snake_case

import os
import sys

from piekit.config import Config, Lock, Max, Min
from pieapp.wizard.wizard import SetupWizard
from piekit.managers.assets.utils import get_palette, get_theme
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager
from piekit.utils.modules import is_debug
from piekit.utils.core import check_crabs
from piekit.utils.core import except_hook
from piekit.utils.core import restore_crabs
from piekit.utils.core import get_application
from piekit.widgets.splashscreen import SplashScreen


def start_application(*args, **kwargs) -> None:
    """
    Main start-up entrypoint
    """
    # Swapping the exception hook
    sys.excepthook = except_hook

    # Adding additional magic-annotations
    Config.add_handlers(Lock, Max, Min)
    
    # Loading configuration modules
    Config.import_module(os.getenv("PIE_SYS_CONFIG_MODULE", "piekit.config.config"))
    Config.import_module(os.getenv("PIE_APP_CONFIG_MODULE", "pieapp.config"))

    # Initializing the `QApplication` instance
    splash = None
    app = get_application(sys.argv)

    # Preparing splash screen
    splash_image = Config.APP_ROOT / Config.ASSETS_FOLDER / "splash.svg"

    if not is_debug() and splash_image.exists():
        splash = SplashScreen(str(splash_image))
        splash.show()

    app.process_events()

    # Preparing or restoring our application's user folder
    if not check_crabs():
        # To prepare/restore user's folder we need to use 
        # only the core managers (Config.INITIAL_MANAGERS)
        restore_crabs()
        for manager in Config.INITIAL_MANAGERS:
            Managers.from_config(manager)

        # Closing splashscreen because we don't need it here
        if splash:
            splash.close()

        # Starting the setup wizard
        wizard = SetupWizard()
        wizard.show()
        sys.exit(app.exec())

    # Preparing our application
    from pieapp.app.main import PieAudioApp
    app = get_application()
    pie_app = PieAudioApp()

    # Starting all managers by order
    for manager in Config.INITIAL_MANAGERS:
        Managers.from_config(manager)

    # Applying *fantasticly* good theme
    theme = Managers(SysManager.Assets).get_theme()
    if theme:
        if Config.ASSETS_USE_STYLE:
            app.set_style_sheet(get_theme(theme))
            palette = get_palette(theme)
            if palette:
                app.set_palette(palette)

    # Closing splashscreen
    if splash:
        splash.close()

    # Start the *magic*
    pie_app.init()

    # Starting all managers by order
    for manager in Config.MANAGERS:
        Managers.from_config(manager)

    pie_app.show()

    sys.exit(app.exec())

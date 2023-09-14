from PySide6.QtCore import QSettings, QCoreApplication
from __feature__ import snake_case

import os
import sys

from piekit.config import Global, Lock, Max, Min
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
    # Adding additional magic-annotations
    Global.add_handlers(Lock, Max, Min)
    
    # Load configuration modules
    Global.import_module(os.getenv("PIE_SYS_GLOBALS_MODULE", "piekit.config.globals"))
    Global.import_module(os.getenv("PIE_APP_GLOBALS_MODULE", "pieapp.globals"))

    # Swapping the exception hook
    if bool(int(Global.USE_EXCEPTION_HOOK)):
        sys.excepthook = except_hook

    # Initializing the `QApplication` instance
    splash = None
    app = get_application(sys.argv)
    app.set_application_name(Global.PIEAPP_APPLICATION_NAME)
    app.set_application_version(Global.PIEAPP_APPLICATION_VERSION)
    app.set_organization_name(Global.PIEAPP_ORGANIZATION_NAME)
    app.set_organization_domain(Global.PIEAPP_ORGANIZATION_DOMAIN)

    # Preparing splash screen
    splash_image = Global.APP_ROOT / Global.ASSETS_FOLDER / "splash.svg"

    if not is_debug() and splash_image.exists():
        splash = SplashScreen(str(splash_image))
        splash.show()

    app.process_events()

    settings = QSettings()
    first_run = settings.value("first_run", type=bool)
    fully_setup = settings.value("fully_setup", type=bool)

    # Preparing or restoring our application's user folder
    if not check_crabs():
        # To prepare/restore user's folder we need to use
        # only the core managers (Config.CORE_MANAGERS)
        restore_crabs()
        settings.set_value("first_run", False)

    if first_run or not fully_setup:
        for manager in Global.CORE_MANAGERS:
            Managers.from_config(manager)

        # Closing splashscreen because we don't need it here
        if splash:
            splash.close()

        # Starting the setup wizard
        wizard = SetupWizard()
        wizard.show()
        sys.exit(app.exec())

    # Preparing our application
    from pieapp.app.main import MainWindow
    app = get_application()
    main_window = MainWindow()

    # Starting all managers by order
    for manager in Global.CORE_MANAGERS:
        Managers.from_config(manager)

    # Applying *fantasticly* good theme
    theme = Managers(SysManager.Assets).get_theme()
    if theme:
        if Global.ASSETS_USE_STYLE:
            app.set_style_sheet(get_theme(theme))
            palette = get_palette(theme)
            if palette:
                app.set_palette(palette)

    # Closing splashscreen
    if splash:
        splash.hide()

    # Start the *magic*
    main_window.prepare_base_signals()
    main_window.prepare_main_window()

    # Starting all managers by order
    for manager in Global.LAYOUT_MANAGERS:
        Managers.from_config(manager)

    main_window.prepare_main_layout()
    main_window.prepare_central_widget()

    Managers.from_config(Global.PLUGIN_MANAGER)

    main_window.show()

    sys.exit(app.exec())

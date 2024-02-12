from PySide6.QtCore import QSettings
from __feature__ import snake_case

import sys
from confstar.types import *

from pieapp.api.globals import Global
from pieapp.api.plugins import Plugins
from pieapp.wizard.wizard import StartupWizard
from pieapp.helpers.modules import is_debug
from pieapp.helpers.qt import get_application, except_hook
from pieapp.widgets.splashscreen import SplashScreen
from pieapp.api.managers.registry import Managers


def check_crabs() -> bool:
    return (
        Global.USER_ROOT.exists()
        and (Global.USER_ROOT / Global.CONFIGS_FOLDER).exists()
        and (Global.USER_ROOT / Global.PLUGINS_FOLDER).exists()
        and (Global.USER_ROOT / Global.CONFIGS_FOLDER / Global.CONFIG_FILE_NAME).exists()
    )


def restore_crabs() -> None:
    if not Global.USER_ROOT.exists():
        Global.USER_ROOT.mkdir()
        (Global.USER_ROOT / Global.CONFIGS_FOLDER).mkdir()
        (Global.USER_ROOT / Global.PLUGINS_FOLDER).mkdir()


def start_application(*args, **kwargs) -> None:
    """
    Main start-up entrypoint
    """
    # Adding additional magic-annotations
    Global.add_handlers(Lock, Max, Min)

    # Load system configuration modules first
    Global.import_module("pieapp.app.globals")

    # Swapping the exception hook
    if bool(int(Global.USE_EXCEPTION_HOOK)):
        sys.excepthook = except_hook

    # Initializing the `QApplication` instance
    splash = None
    app = get_application(sys.argv)
    app.set_application_name(Global.PIEAPP_APPLICATION_NAME)
    app.set_application_version(Global.PIEAPP_VERSION)
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
            Managers.from_string(manager)

        app.set_style_sheet("")

        # Closing splashscreen because we don't need it here
        if splash:
            splash.close()

        # Starting the setup wizard
        wizard = StartupWizard()
        wizard.show()
        sys.exit(app.exec())

    # Preparing our application
    # Starting all managers by order
    for manager in Global.CORE_MANAGERS:
        Managers.from_string(manager)

    from pieapp.app.main import MainWindow
    app = get_application()
    main_window = MainWindow()

    # Closing splashscreen
    if splash:
        splash.hide()

    # Starting all managers by order
    for manager in Global.LAYOUT_MANAGERS:
        Managers.from_string(manager)

    Plugins.init_plugins()

    main_window.show()

    sys.exit(app.exec())

import sys

from PySide6.QtCore import QSettings
from __feature__ import snake_case

from pieapp.utils.qt import except_hook
from pieapp.utils.qt import get_application
from pieapp.utils.modules import is_debug
from pieapp.utils.files import check_user_folders
from pieapp.utils.files import restore_user_folders

from pieapp.api.gloader import Global
from pieapp.api.registries.registry import Registry

from pieapp.app.wizard.wizard import StartupWizard
from pieapp.widgets.splashscreen import SplashScreen


def start_application(*args, **kwargs) -> None:
    """
    Main start-up entrypoint
    """
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

    # Check and restore user folder essential files
    if not check_user_folders():
        # To prepare/restore user's folder we need to use
        # only the core managers (Global.CORE_MANAGERS)
        restore_user_folders()
        settings.set_value("first_run", True)

    first_run = settings.value("first_run", type=bool)
    if first_run:
        for manager in Global.CORE_MANAGERS:
            Registry.init_from_string(manager)

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
        Registry.init_from_string(manager)

    from pieapp.app.main import MainWindow
    app = get_application()
    main_window = MainWindow()

    # Starting all managers by order
    for manager in Global.LAYOUT_MANAGERS:
        Registry.init_from_string(manager)

    main_window.init()
    main_window.show()

    if splash:
        splash.close()

    sys.exit(app.exec())

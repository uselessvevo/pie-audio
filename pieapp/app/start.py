import sys

from PySide6.QtCore import QSettings
from __feature__ import snake_case

from pieapp.api.plugins import PluginRegistry
from pieapp.api.utils.errorhook import exception_hook
from pieapp.api.utils.qapp import get_application
from pieapp.api.utils.modules import is_debug
from pieapp.api.utils.files import check_user_folders
from pieapp.api.utils.files import restore_user_folders

from pieapp.api.globals import Global
from pieapp.api.registries.registry import RegistryContainer

from pieapp.app.wizard.wizard import StartupWizard
from pieapp.widgets.splashscreen import SplashScreen


def start_application(*args, **kwargs) -> None:
    """
    Main start-up entrypoint
    """
    # Load globals from the application directory
    Global.import_module("pieapp.app.globals")

    # Swapping the exception hook
    # if bool(int(Global.USE_EXCEPTION_HOOK)):
    #     sys.excepthook = exception_hook

    # Initialize "QApplication" instance
    splash = None
    app = get_application(sys.argv)
    app.set_application_name(Global.PIEAPP_APPLICATION_NAME)
    app.set_application_version(Global.PIEAPP_VERSION)
    app.set_organization_name(Global.PIEAPP_ORGANIZATION_NAME)
    app.set_organization_domain(Global.PIEAPP_ORGANIZATION_DOMAIN)

    # Prepare splash screen image
    splash_image = Global.APP_ROOT / Global.ASSETS_DIR_NAME / "splash.svg"
    if not is_debug() and splash_image.exists():
        splash = SplashScreen(str(splash_image))
        splash.show()

    settings = QSettings()

    # Check if user folders exist
    if not check_user_folders():
        # Restore user folders
        # and update system configuration key "FreshStart"
        restore_user_folders()
        settings.set_value("FreshStart", True)

    fresh_start = settings.value("FreshStart", type=bool)
    if fresh_start is True:
        # We only need core registries to configure our app
        for manager in Global.CORE_REGISTRIES:
            RegistryContainer.init_from_string(manager)

        app.set_style_sheet("")

        if splash is not None:
            splash.close()

        # Start the setup wizard
        wizard = StartupWizard()
        wizard.show()
        sys.exit(app.exec())

    # Initialize all core registries
    for manager in Global.CORE_REGISTRIES:
        RegistryContainer.init_from_string(manager)

    from pieapp.app.main import MainWindow
    main_window = MainWindow()

    # Initialize all layout registries
    for manager in Global.LAYOUT_REGISTRIES:
        RegistryContainer.init_from_string(manager)

    # Initialize plugin registry and all plugins
    PluginRegistry.init_plugins()

    # Initialize main window
    main_window.init()

    if splash is not None:
        splash.close()

    sys.exit(app.exec())

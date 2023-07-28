import os

from piekit.config.types import Lock
from piekit.managers.structs import DirectoryType
from piekit.managers.structs import ManagerConfig


# Application main info
PIEAPP_APPLICATION_NAME: Lock = "pie-audio"
PIEAPP_APPLICATION_VERSION: Lock = "1.0.0"
PIEAPP_ORGANIZATION_NAME: Lock = "Crab Devs."
PIEAPP_ORGANIZATION_DOMAIN: Lock = "com.crabdevs.pieaudio"

PIEAPP_PROJECT_URL = "https://github.com/uselessvevo/pie-audio/"

MAIN_WINDOW_MIN_WINDOW_SIZE: Lock = (720, 480)

# List of excluded file formats
ASSETS_EXCLUDED_FORMATS = [DirectoryType, ".qss", ".json", ".ttf", ".py"]
USE_EXCEPTION_HOOK: Lock = os.getenv("PIE_USE_EXCEPTION_HOOK", True)

DEFAULT_CONFIG_FILES = [
    "locales.json",
    "assets.json",
    "ffmpeg.json",
]

USE_TEST_PLUGIN = os.getenv("PIE_USE_TEST_PLUGIN", False)

# Managers startup configuration
INITIAL_MANAGERS: Lock = [
    ManagerConfig(
        import_string="piekit.managers.configs.manager.ConfigManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.locales.manager.LocaleManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.assets.manager.AssetsManager",
        init=True
    ),
]

MANAGERS: Lock = [
    *INITIAL_MANAGERS,
    ManagerConfig(
        import_string="piekit.managers.menus.manager.MenuManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.toolbars.manager.ToolBarManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.toolbuttons.manager.ToolButtonManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.confpages.manager.ConfigPageManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.plugins.manager.PluginManager",
        init=True
    ),
]

from piekit.config.types import Lock
from piekit.managers.structs import DirectoryType
from piekit.managers.structs import ManagerConfig


# Application main info
PIEAPP_NAME: Lock = "pie-audio"
PIEAPP_VERSION: Lock = "1.0.0"
PIEAPP_PROCESS_NAME_ID = "com.crabdevs.pieaudio"

MAIN_WINDOW_DEFAULT_WINDOW_SIZE: Lock = (900, 560)

# List of excluded file formats
ASSETS_EXCLUDED_FORMATS = [DirectoryType, ".qss", ".json", ".ttf", ".py"]

# Configuration pages
CONF_PAGES_CATEGORIES = [
    {"title": "Main", "name": "main"},
    {"title": "Plugins", "name": "plugins"},
]

# Managers startup configuration
# TODO: Replace `init` attribute with Qt signal name (str) and emit it via `QMetaObject` -> `invokeMethod`
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
        import_string="piekit.managers.plugins.manager.PluginManager",
        init=False
    ),
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
    )
]

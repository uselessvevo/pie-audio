import os

from PySide6.QtWidgets import QGridLayout

from piekit.globals.types import Lock
from piekit.managers.structs import DirectoryType


# Application main info
PIEAPP_APPLICATION_NAME: Lock = "pie-audio"
PIEAPP_APPLICATION_VERSION: Lock = "1.0.0"
PIEAPP_ORGANIZATION_NAME: Lock = "Crab Devs."
PIEAPP_ORGANIZATION_DOMAIN: Lock = "com.crabdevs.pieaudio"
PIEAPP_PROJECT_URL = "https://github.com/uselessvevo/pie-audio/"

MAIN_GRID_LAYOUT_CLASS: Lock = QGridLayout
DEFAULT_MIN_WINDOW_SIZE: Lock = (720, 500)
TOOL_BUTTON_ICON_SIZE: Lock = (25, 25)

# List of excluded file formats
ASSETS_EXCLUDED_FORMATS = [DirectoryType, ".qss", ".json", ".ttf", ".py"]
USE_EXCEPTION_HOOK: Lock = os.getenv("PIE_USE_EXCEPTION_HOOK", True)

# Managers startup configuration
CORE_MANAGERS: Lock = [
    "piekit.managers.configs.manager.ConfigManager",
    "piekit.managers.locales.manager.LocaleManager",
    "piekit.managers.assets.manager.AssetsManager",
]

LAYOUT_MANAGERS: Lock = [
    "piekit.managers.menus.manager.MenuManager",
    "piekit.managers.toolbars.manager.ToolBarManager",
    "piekit.managers.toolbuttons.manager.ToolButtonManager",
    "piekit.managers.confpages.manager.ConfigPageManager",
    "piekit.managers.layouts.manager.LayoutManager",
]

PLUGIN_MANAGER = "piekit.managers.plugins.manager.PluginManager"

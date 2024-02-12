import locale
import os.path
from pathlib import Path

from confstar.types import Lock

PIEKIT_VERSION: Lock = "1.0.0"

# Base paths
BASE_DIR: Lock = Path(__file__).parent.parent.parent
APP_ROOT: Lock = BASE_DIR / os.getenv("PIE_APP_ROOT", "pieapp")
USER_ROOT: Lock = Path.home() / ".crabs"

LOG_LEVEL = os.getenv("PIE_LOG_LEVEL", "DEBUG")

PLUGINS_SIGNAL_PREFIX: Lock = "sig_"
PLUGINS_PRIVATE_SIGNALS: Lock = ("sig_plugin_ready",)

# Default temporary folder
DEFAULT_TEMP_FOLDER_NAME: Lock = "temp"

# Plugins configuration
# Built-in plugins folder
DEFAULT_PLUGIN_ICON_NAME: Lock = "app"
PLUGINS_FOLDER: Lock = "plugins"

# Configuration pages
CONF_PAGES_FOLDER: Lock = "app"

# User's/third-party plugins folder
USER_PLUGINS_FOLDER: Lock = "plugins"

# Assets
ASSETS_FOLDER: Lock = "assets"

# Icons
ICONS_ALLOWED_FORMATS = [".svg", ".png", ".ico"]

themes_list = tuple(i for i in (APP_ROOT / ASSETS_FOLDER).rglob("*") if i.is_dir())
DEFAULT_THEME: Lock = themes_list[0].name if themes_list else None
USE_THEME: Lock = bool(int(os.getenv("PIE_USE_THEME", True)))

# Configurations
CONFIG_FILE_NAME: Lock = "config.json"
CONFIGS_FOLDER: Lock = "configs"
USER_CONFIG_FOLDER: Lock = "configs"

# Locales
LOCALES = {
    "en-US": "English",
    "ru-RU": "Русский"
}

# Setup default locale
system_locale = locale.getdefaultlocale()[0].replace("_", "-")
default_locale = system_locale if system_locale in LOCALES else "en-US"

DEFAULT_LOCALE: Lock = default_locale
LOCALES_FOLDER: Lock = "locales"


# Application globals

# Application main info
PIEAPP_APPLICATION_NAME: Lock = "pie-audio"
PIEAPP_VERSION: Lock = "1.0.0"
PIEAPP_ORGANIZATION_NAME: Lock = "Crab Devs."
PIEAPP_ORGANIZATION_DOMAIN: Lock = "com.crabdevs.pieaudio"
PIEAPP_PROJECT_URL = "https://github.com/uselessvevo/pie-audio/"

DEFAULT_MIN_WINDOW_SIZE: Lock = (760, 480)
TOOL_BUTTON_ICON_SIZE: Lock = (24, 24)

# List of excluded file formats
USE_EXCEPTION_HOOK: Lock = os.getenv("PIE_USE_EXCEPTION_HOOK", True)

# Managers startup configuration
CORE_MANAGERS: Lock = [
    "pieapp.api.managers.configs.manager.ConfigManager",
    "pieapp.api.managers.locales.manager.LocaleManager",
    "pieapp.api.managers.themes.manager.ThemeManager",
]

LAYOUT_MANAGERS: Lock = [
    "pieapp.api.managers.layouts.manager.LayoutManager",
    "pieapp.api.managers.menus.manager.MenuManager",
    "pieapp.api.managers.toolbars.manager.ToolBarManager",
    "pieapp.api.managers.toolbuttons.manager.ToolButtonManager",
    "pieapp.api.managers.shortcuts.manager.ShortcutManager",
]

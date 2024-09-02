import locale
import os.path
from pathlib import Path


# Base configuration fields #
PIEKIT_VERSION = "1.0.0"

# Base/root project folder
BASE_DIR = Path(__file__).parent.parent.parent

# Application root folder
APP_ROOT = BASE_DIR / os.getenv("PIE_APP_ROOT", "pieapp")

# User root folder
USER_ROOT = Path.home() / ".pie"

# Default temporary folder name
DEFAULT_TEMP_FOLDER_NAME = "temp"
MEDIA_FILES_FOLDER_NAME = "media"

# Logging fields #

LOG_LEVEL = os.getenv("PIE_LOG_LEVEL", "DEBUG")

# Default plugin icon theme
DEFAULT_PLUGIN_ICON_NAME = "app"

# Plugin folder name
PLUGINS_FOLDER_NAME = "plugins"

# Configuration pages fields #

# Configuration pages folder name
CONF_PAGES_FOLDER = "app"

# User's/third-party plugins folder
USER_PLUGINS_FOLDER = "plugins"

# Assets/theme fields #
# Assets folder name
ASSETS_FOLDER = "assets"

# Icons allowed formats list
ICONS_ALLOWED_FORMATS = [".svg", ".png", ".ico"]

_themes_list = tuple(i for i in (APP_ROOT / ASSETS_FOLDER).rglob("*") if i.is_dir())
DEFAULT_THEME = _themes_list[0].name if _themes_list else None
USE_THEME = bool(int(os.getenv("PIE_USE_THEME", True)))

# Configuration fields #
CONFIG_FILE_NAME = "config.json"
CONFIGS_FOLDER_NAME = "configs"

# Locales fields #

LOCALES = {
    "en_US": "English",
    "ru_RU": "Русский"
}

# Setup default locale
_system_locale = locale.getdefaultlocale()[0]
default_locale = _system_locale if _system_locale in LOCALES else "en_US"

DEFAULT_LOCALE = default_locale
LOCALES_FOLDER = "locales"

# Application related fields #

# Main information
PIEAPP_APPLICATION_NAME = "pie-audio"
PIEAPP_VERSION = "1.0.3"
PIEAPP_VERSION_STAGE = "alpha"
PIEAPP_ORGANIZATION_NAME = "CrabDevs"
PIEAPP_ORGANIZATION_DOMAIN = "com.crabdevs.pieaudio"
PIEAPP_PROJECT_URL = "https://github.com/uselessvevo/pie-audio/"

DEFAULT_MIN_WINDOW_SIZE = (760, 480)
TOOL_BUTTON_ICON_SIZE = (24, 24)

IS_DEV_ENV = os.getenv("PIE_IS_DEV_ENV", False)
FFMPEG_RELEASE_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest"

# List of excluded file formats
USE_EXCEPTION_HOOK = os.getenv("PIE_USE_EXCEPTION_HOOK", True)

# Managers startup configuration
CORE_MANAGERS = [
    "pieapp.api.registries.configs.manager.Configs",
    "pieapp.api.registries.locales.manager.Locales",
    "pieapp.api.registries.themes.manager.Themes",
    "pieapp.api.registries.snapshots.manager.Snapshots"
]

LAYOUT_MANAGERS = [
    "pieapp.api.registries.layouts.manager.Layouts",
    "pieapp.api.registries.menus.manager.Menus",
    "pieapp.api.registries.toolbars.manager.ToolBars",
    "pieapp.api.registries.toolbuttons.manager.ToolButtons",
    "pieapp.api.registries.shortcuts.manager.Shortcuts",
    "pieapp.api.registries.confpages.manager.ConfigPages",
]

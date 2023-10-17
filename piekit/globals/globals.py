import locale
import os.path
from pathlib import Path

from piekit.globals.types import Lock

PIEKIT_VERSION: Lock = "1.0.0"

# Base paths
BASE_DIR: Lock = Path(__file__).parent.parent.parent
APP_ROOT: Lock = BASE_DIR / os.getenv("PIE_APP_ROOT", "pieapp")
USER_ROOT: Lock = Path.home() / ".crabs"
SYSTEM_ROOT: Lock = BASE_DIR / "piekit"

# Plugins configuration
# Built-in plugins folder
DEFAULT_PLUGIN_ICON_NAME: Lock = "app"
PLUGINS_FOLDER: Lock = "plugins"

# Configuration pages
CONF_PAGES_FOLDER: Lock = "app"

# User's/third-party plugins folder
USER_PLUGINS_FOLDER: Lock = "plugins"

# Assets
ASSETS_EXCLUDED_FORMATS: list = []
ASSETS_FOLDER: Lock = "assets"
THEMES_FOLDER: Lock = "themes"

themes_list = tuple(i for i in (APP_ROOT / ASSETS_FOLDER).rglob("*") if i.is_dir())
DEFAULT_THEME: Lock = themes_list[0] if themes_list else None
ASSETS_USE_STYLE: Lock = bool(int(os.getenv("PIE_ASSETS_USE_STYLE", False)))

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

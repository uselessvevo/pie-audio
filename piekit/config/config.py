import locale
import os.path
from pathlib import Path

from piekit.config.types import Lock

PIEKIT_VERSION: Lock = "1.0.0"

# Base paths
BASE_DIR: Lock = Path(__file__).parent.parent.parent
APP_ROOT: Lock = BASE_DIR / os.getenv("PIE_APP_ROOT", "pieapp")
USER_ROOT: Lock = os.getenv("PIE_USER_ROOT", Path.home() / ".crabs")
SYSTEM_ROOT: Lock = BASE_DIR / "piekit"

# Plugins configuration
# Built-in plugins folder
PLUGINS_FOLDER: Lock = os.getenv("PIE_PLUGINS_FOLDER", "plugins")

# Configuration pages
CONF_PAGES_FOLDER: Lock = os.getenv("PIE_CONF_PAGES_FOLDER", "app")
CONF_PAGES_CATEGORIES: list[dict] = []

# User/site plugins folder
USER_PLUGINS_FOLDER: Lock = os.getenv("PIE_USER_PLUGINS_FOLDER", "plugins")

# Components folder
COMPONENTS_FOLDER: Lock = os.getenv("PIE_COMPONENTS_FOLDER", "components")

# Containers folder
CONTAINERS_FOLDER: Lock = os.getenv("PIE_CONTAINERS_FOLDER", "containers")

# Assets
ASSETS_EXCLUDED_FORMATS: list = []
ASSETS_FOLDER: Lock = os.getenv("PIE_ASSETS_FOLDER", "assets")
THEMES_FOLDER: Lock = os.getenv("PIE_THEMES_FOLDER", "themes")

themes_list = tuple(i for i in (APP_ROOT / ASSETS_FOLDER).rglob("*") if i.is_dir())
DEFAULT_THEME: Lock = themes_list[0] if themes_list else None
ASSETS_USE_STYLE: Lock = bool(os.getenv("PIE_ASSETS_USE_STYLE", True))

# Configurations
CONFIGS_FOLDER: Lock = os.getenv("PIE_CONFIGS_FOLDER", "configs")
USER_CONFIG_FOLDER: Lock = os.getenv("PIE_USER_CONFIGS_FOLDER", "configs")

# Locales
LOCALES: Lock = {
    "en-US": "English",
    "ru-RU": "Русский"
}

# Setup default locale
system_locale = locale.getdefaultlocale()[0].replace("_", "-")
default_locale = system_locale if system_locale in LOCALES else "en-US"

DEFAULT_LOCALE: Lock = os.getenv("PIE_DEFAULT_LOCALE", default_locale)
LOCALES_FOLDER: Lock = os.getenv("PIE_LOCALES_FOLDER", "locales")

# Templates
DEFAULT_CONFIG_FILES: Lock = [
    "locales.json",
    "assets.json",
    "ffmpeg.json",
]

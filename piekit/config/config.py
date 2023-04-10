import locale
import os.path
from pathlib import Path

from piekit.config.types import Lock
from piekit.managers.structs import ManagerConfig

# Base paths
BASE_DIR: Lock = Path(__file__).parent.parent.parent
APP_ROOT: Lock = BASE_DIR / os.getenv("PIEADUIO_ROOT", "pieapp")
USER_ROOT: Lock = os.getenv("USER_ROOT", Path.home() / ".crabs")
SYSTEM_ROOT: Lock = BASE_DIR / "piekit"

# Plugins configuration
# Built-in plugins folder
PLUGINS_FOLDER: Lock = os.getenv("PLUGINS_FOLDER", "plugins")

# User/site plugins folder
USER_PLUGINS_FOLDER: Lock = os.getenv("USER_PLUGINS_FOLDER", "plugins")

# Components folder
COMPONENTS_FOLDER: Lock = os.getenv("COMPONENTS_FOLDER", "components")

# Containers folder
CONTAINERS_FOLDER: Lock = os.getenv("CONTAINERS_FOLDER", "containers")

# Assets
ASSETS_EXCLUDED_FORMATS: list = []
ASSETS_FOLDER: Lock = os.getenv("ASSETS_FOLDER", "assets")
THEMES_FOLDER: Lock = os.getenv("THEMES_FOLDER", "themes")
DEFAULT_THEME = tuple(i for i in (APP_ROOT / ASSETS_FOLDER).rglob("*") if i.is_dir())[0]
ASSETS_USE_STYLE: bool = bool(os.getenv("ASSETS_USE_STYLE", True))

# Configurations
CONFIGS_FOLDER: Lock = os.getenv("CONFIGS_FOLDER", "configs")
USER_CONFIG_FOLDER: Lock = os.getenv("USER_CONFIGS_FOLDER", "configs")
USER_FOLDER_FILES: Lock = ["locales.json", "assets.json"]

# Locales
LOCALES: Lock = {
    "en-US": "English",
    "ru-RU": "Русский"
}

# Setup default locale
system_locale = locale.getdefaultlocale()[0].replace("_", "-")
default_locale = system_locale if system_locale in LOCALES else "en-US"

DEFAULT_LOCALE: Lock = os.getenv("DEFAULT_LOCALE", default_locale)
LOCALES_FOLDER: Lock = os.getenv("LOCALES_FOLDER", "locales")


# Templates
TEMPLATE_FILES: Lock = [
    "locales.json",
    "assets.json",
    "ffmpeg.json",
]


# Managers startup configuration
# TODO: Replace `init` attribute with Qt signal name (str) and emit it via `QMetaObject` -> `invokeMethod`
MANAGERS: Lock = [
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

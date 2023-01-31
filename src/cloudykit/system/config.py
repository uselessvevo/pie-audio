import locale
import os.path
from pathlib import Path

from cloudykit.system.types import EList
from cloudykit.system.types import EDict
from cloudykit.system.types import PathConfig
from cloudykit.system.types import ManagerConfig


# Base paths
BASE_DIR: Path = Path(__file__).parent.parent.parent
APP_ROOT: Path = BASE_DIR / os.getenv("CLOUDYAPP_ROOT", "cloudyapp")
USER_ROOT: Path = os.getenv("USER_ROOT", Path.home() / ".crabs")
SYSTEM_ROOT: Path = BASE_DIR / "cloudykit"

CLOUDYAPP_ENTRYPOINT = os.getenv("CLOUDYAPP_ENTRYPOINT", "main.main")

# List of plugins. By default, it's empty
# String must be like this: `plugin_name`
PLUGINS_FOLDER: str = os.getenv("PLUGINS_FOLDER", "plugins")
USER_PLUGINS_FOLDER: str = os.getenv("USER_PLUGINS_FOLDER", "plugins")  # requires `ConfigManager`


# List of components. By default, it's empty
# String must be like this: `path.to.component.package`
# For example, `cloudyapp.components.workbench`
COMPONENTS_FOLDER: str = os.getenv("COMPONENTS_FOLDER", "components")
COMPONENTS: EList = []


# Assets
ASSETS_EXCLUDED_FORMATS: EList = []
ASSETS_FOLDER: str = os.getenv("ASSETS_FOLDER", "assets")
THEMES_FOLDER: str = os.getenv("THEMES_FOLDER", "themes")


# Configurations
CONFIGS_FOLDER = os.getenv("CONFIGS_FOLDER", "configs")
USER_CONFIG_FOLDER: str = os.getenv("USER_CONFIGS_FOLDER", "configs")
USER_FOLDER_FILES: EList = ["locales.json", "assets.json"]

# Templates
TEMPLATE_FOLDER: str = "templates"

# Locales
LOCALES: EDict = {
    "en-US": "English",
    "ru-RU": "Русский"
}

# Setup default locale
system_locale = locale.getdefaultlocale()[0].replace("_", "-")
default_locale = system_locale if system_locale in LOCALES else "en-US"

DEFAULT_LOCALE: str = os.getenv("DEFAULT_LOCALE", default_locale)
LOCALES_FOLDER: str = os.getenv("LOCALES_FOLDER", "locales")


# Managers startup configuration
# TODO: Replace `mount` attribute with Qt signal name (str) and emit it via `QMetaObject` -> `invokeMethod`
MANAGERS: EList = [
    ManagerConfig(
        import_string="cloudykit.managers.configs.manager.ConfigManager",
        mount=True,
        args=(
            PathConfig(APP_ROOT / USER_CONFIG_FOLDER, section="shared"),
            PathConfig(USER_ROOT / USER_CONFIG_FOLDER, section="user")
        )
    ),
    ManagerConfig(
        import_string="cloudykit.managers.locales.manager.LocalesManager",
        mount=True,
        args=(PathConfig(APP_ROOT / LOCALES_FOLDER, section="shared"),)
    ),
    ManagerConfig(
        import_string="cloudykit.managers.assets.manager.AssetsManager",
        mount=True,
        args=(PathConfig(APP_ROOT / ASSETS_FOLDER, pattern="*", section="shared"),)
    ),
    ManagerConfig(
        import_string="cloudykit.managers.components.manager.ComponentsManager",
        mount=False
    ),
    ManagerConfig(
        import_string="cloudykit.managers.plugins.manager.PluginsManager",
        mount=False
    )
]

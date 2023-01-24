import os.path
from pathlib import Path

from cloudykit.system.types import EList, EDict, ManagerConfig, PathConfig

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
APP_ROOT = BASE_DIR / os.getenv("CLOUDYAPP_ROOT", "cloudyapp")

# List of plugins. By default, it's empty
# String must be like this: `plugin_name`
PLUGINS_FOLDER: str = "plugins"
PLUGINS_USER_FOLDER: str = "plugins"  # requires `ConfigManager`


# List of components. By default, it's empty
# String must be like this: `path.to.component.package`
# For example, `cloudyapp.components.workbench`
COMPONENTS_FOLDER: str = "components"
COMPONENTS: EList = []


# Assets
ASSETS_EXCLUDED_FORMATS: EList = []
ASSETS_FOLDER: str = os.getenv("ASSETS_FOLDER", "assets")
THEMES_FOLDER: str = os.getenv("THEMES_FOLDER", "themes")


# Configurations
CONFIGS_FOLDER = os.getenv("CONFIGS_FOLDER", "configs")
USER_CONFIG_FOLDER: str = os.getenv("USER_CONFIGS_FOLDER") or f"{os.path.expanduser('~')}/.crabs"
USER_FOLDER_FILES: EList = ["locales.json", "assets.json"]


# Locales
DEFAULT_LOCALE = os.getenv("DEFAULT_LOCALE", "en-US")
LOCALES_FOLDER: str = "locales"
LOCALES: EDict = {
    "en-US": "English",
    "ru-RU": "Русский"
}
SHARED_TYPE: str = "shared"


# Managers startup configuration
# TODO: Replace `mount` attribute with Qt signal name (str) and emit it via `QMetaObject` -> `invokeMethod`
MANAGERS: EList = [
    ManagerConfig(
        import_string="cloudykit.managers.configs.manager.ConfigManager",
        mount=True,
        args=(PathConfig(Path(USER_CONFIG_FOLDER), section="user", section_stem=False),)
    ),
    ManagerConfig(
        import_string="cloudykit.managers.locales.manager.LocalesManager",
        mount=True
    ),
    ManagerConfig(
        import_string="cloudykit.managers.assets.manager.AssetsManager",
        mount=True
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

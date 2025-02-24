import locale
import os.path
from pathlib import Path


"""
Application related fields
"""

# API version
PIEKIT_VERSION = "1.0.4"

# Applicatio name
PIEAPP_APPLICATION_NAME = "pie-audio"

# Application version
PIEAPP_VERSION = "1.0.4"

# This field is used to show in what stage app is
PIEAPP_VERSION_STAGE = "alpha"

# Organization name
PIEAPP_ORGANIZATION_NAME = "CrabDevs"

# Organization domain
PIEAPP_ORGANIZATION_DOMAIN = "com.crabdevs.pieaudio"

# Project URL
PIEAPP_PROJECT_URL = "https://github.com/uselessvevo/pie-audio/"


"""
Directories fields
"""

# Project root directory
BASE_DIR = Path(__file__).parent.parent.parent

# Application root folder
APP_ROOT = BASE_DIR / os.getenv("PIE_APP_ROOT", "pieapp")

# User root folder
USER_ROOT = Path.home() / ".pie"

# Temporary folder name
DEFAULT_TEMP_DIR_NAME = "temp"

# Media folder name
MEDIA_FILES_DIR_NAME = "media"

# Output folder name
OUTPUT_DIR_NAME = "output"

# Default plugin icon theme
DEFAULT_PLUGIN_ICON_NAME = "app"

# Plugin folder name
PLUGINS_DIR_NAME = "plugins"

"""
Assets fields
"""

# Assets folder name
ASSETS_DIR_NAME = "assets"

# Icons allowed formats list
ICONS_ALLOWED_FORMATS = [".svg", ".png", ".ico"]

_themes_list = tuple(i for i in (APP_ROOT / ASSETS_DIR_NAME).rglob("*") if i.is_dir())
DEFAULT_THEME = _themes_list[0].name if _themes_list else None
USE_THEME = bool(int(os.getenv("PIE_USE_THEME", True)))


"""
Configuration fields
"""

CONFIG_FILE_NAME = "config"
CONFIGS_DIR_NAME = "configs"
APP_CONFIG_FILES = (
    "config.json",
    "ffmpeg.json",
    "workflow.json",
)

# Locales fields #

LOCALES = {
    "en_US": "English",
    "ru_RU": "Русский"
}

# Setup default locale
_system_locale = locale.getdefaultlocale()[0]
default_locale = _system_locale if _system_locale in LOCALES else "en_US"

DEFAULT_LOCALE = default_locale
LOCALES_DIR = "locales"

DEFAULT_WINDOW_SIZE = (760, 480)

IS_DEV_ENV = os.getenv("PIE_IS_DEV_ENV", False)
FFMPEG_RELEASE_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest"

# List of excluded file formats
USE_EXCEPTION_HOOK = os.getenv("PIE_USE_EXCEPTION_HOOK", True)

"""
Registries configuration fields
"""

CORE_REGISTRIES = [
    "pieapp.api.registries.configs.registry.ConfigRegistry",
    "pieapp.api.registries.locales.registry.LocaleRegistry",
    "pieapp.api.registries.themes.registry.ThemeRegistry",
    "pieapp.api.registries.snapshots.registry.SnapshotRegistry"
]

LAYOUT_REGISTRIES = [
    "pieapp.api.registries.layouts.registry.LayoutRegistry",
    "pieapp.api.registries.shortcuts.registry.ShortcutRegistry",
    "pieapp.api.registries.confpages.registry.ConfigPageRegistry",
    "pieapp.api.registries.menus.registry.MenuRegistry",
    "pieapp.api.registries.tabs.registry.TabRegistry",
    "pieapp.api.registries.toolbars.registry.ToolBarRegistry",
    "pieapp.api.registries.toolbuttons.registry.ToolButtonRegistry",
    "pieapp.api.registries.quickactions.registry.QuickActionRegistry"
]
ALBUM_COVER_EXTENSIONS = [
    "jpeg", "jpg", "png",
]
AUDIO_EXTENSIONS = [
    "m3u", "m3u8", "au", "snd", "mp3", "mp2", "aif",
    "aifc", "aiff", "ra", "wav", "mpa", "aa", "aac",
    "aax", "ac3", "adt", "adts", "ape", "ec3", "flac",
    "lpcm", "m4b", "m4p", "m4r", "mid", "midi", "mka",
    "mpc", "oga", "ogg", "opus", "pls", "rmi", "tak",
    "wave", "wax", "weba", "wma", "wv", "m4a", "ogg",
    "wav",
]
IMAGE_EXTENSIONS = [
    "bmp", "gif", "ief", "jpg", "jpe", "jpeg", "png",
    "svg", "tiff", "tif", "ico", "ras", "pnm", "pbm",
    "pgm", "ppm", "rgb", "xbm", "xpm", "xwd", "3fr",
    "ari", "arw", "bay", "cap", "cb7", "cbr", "cbz",
    "cr2", "cr3", "crw", "dcr", "dcs", "dds", "dib",
    "dng", "drf", "eip", "emf", "erf", "fff", "iiq",
    "jfif", "jxr", "k25", "kdc", "mef", "mos", "mrw",
    "nef", "nrw", "orf", "ori", "pef", "ptx", "pxn",
    "raf", "raw", "rw2", "rwl", "sr2", "srw", "wdp",
    "webp", "wmf", "x3f"
]

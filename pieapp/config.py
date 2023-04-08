from piekit.managers.structs import DirectoryType
from piekit.config.types import Lock

PIEAPP_VERSION: Lock = "2023.04.pre-alpha"

# List of excluded file formats
ASSETS_EXCLUDED_FORMATS = [DirectoryType, ".qss", ".json", ".ttf", ".py"]

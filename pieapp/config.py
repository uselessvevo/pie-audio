from piekit.system.types import elist, edict
from piekit.managers.structs import DirectoryType

PIEAPP_VERSION: str = "2023.04.pre-alpha"

# List of excluded file formats
ASSETS_EXCLUDED_FORMATS: elist = [DirectoryType, ".qss", ".json", ".ttf", ".py"]

# QToolButton icon size
TOOL_BUTTON_ICON_SIZE: tuple = (25, 25)

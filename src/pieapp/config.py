from piekit.structs.etypes import EList
from piekit.structs.etc import DirectoryType

# List of excluded file formats
ASSETS_EXCLUDED_FORMATS: EList = [DirectoryType, ".qss", ".json", ".ttf", ".py"]

# List of built-in plugins
PLUGINS_LOADING_ORDER: EList = [
    "preferences",
    "shorcuts",
    "testplugin"
]

from cloudykit.system import EList, DirectoryType


# List of excluded file formats
ASSETS_EXCLUDED_FORMATS: EList = [DirectoryType, ".qss", ".json", ".ttf", ".py"]

# List of built-in plugins
PLUGINS_LOADING_ORDER: EList = [
    "preferences",
    "shorcuts",
    "testplugin"
]

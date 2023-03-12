"""
Plugin helpers
"""
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers
from piekit.plugins.plugins import PiePlugin


def get_plugin(plugin: str) -> PiePlugin:
    return Managers(SysManagers.Plugins)(plugin)


getPlugin = get_plugin

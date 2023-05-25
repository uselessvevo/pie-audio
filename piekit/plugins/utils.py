"""
Plugin helpers
"""
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager
from piekit.plugins.plugins import PiePlugin


def get_plugin(plugin: str) -> PiePlugin:
    return Managers(SysManager.Plugins).get(plugin)


getPlugin = get_plugin

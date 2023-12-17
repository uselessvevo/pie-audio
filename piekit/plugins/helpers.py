"""
Plugin helpers
"""
from piekit.plugins.plugins import PiePlugin
from piekit.plugins.registry import Plugins


def get_plugin(plugin: str) -> PiePlugin:
    return Plugins.get_plugin(plugin)

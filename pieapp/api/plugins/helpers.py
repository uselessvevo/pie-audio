"""
Plugin utils
"""
from typing import Any

from pieapp.api.plugins.registry import PluginRegistry


def get_plugin(plugin: str) -> Any:
    return PluginRegistry.get_plugin(plugin)


def get_plugin_widget(plugin: str) -> Any:
    return PluginRegistry.get_plugin(plugin).get_widget()

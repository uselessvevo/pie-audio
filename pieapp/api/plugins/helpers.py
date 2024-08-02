"""
Plugin utils
"""
from typing import Any

from pieapp.api.plugins.registry import Plugins


def get_plugin(plugin: str) -> Any:
    return Plugins.get_plugin(plugin)

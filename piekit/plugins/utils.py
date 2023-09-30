"""
Plugin helpers
"""
from typing import Any

from piekit.exceptions import PieException
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager
from piekit.plugins.plugins import PiePlugin
from piekit.plugins.api import PiePluginAPI


def get_plugin(plugin: str) -> PiePlugin:
    return Managers(SysManager.Plugins).get(plugin)


def get_api(plugin: str, method: str, **kwargs) -> Any:
    plugin_instance = get_plugin(plugin)
    if not plugin_instance.api:
        raise PieException(f"Plugin \"{plugin}\" has no controller implementation")

    if not isinstance(plugin_instance.api, PiePluginAPI):
        raise PieException(f"Plugin \"{plugin}\" has incorrect controller instance type")

    return plugin_instance.api.call(method, **kwargs)


getAPI = get_api
getPlugin = get_plugin

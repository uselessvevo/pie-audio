"""
API helpers
"""
from typing import Any

from piekit.plugins.api.api import PiePluginAPI
from piekit.plugins.api.exceptions import NoApiImplementationError
from piekit.plugins.helpers import get_plugin


def get_api(plugin: str, method: str, **kwargs) -> Any:
    plugin_instance = get_plugin(plugin)
    if not isinstance(plugin_instance.api, PiePluginAPI):
        raise NoApiImplementationError(plugin)

    return plugin_instance.api(method, **kwargs)


getAPI = get_api

import functools
from typing import Callable, Optional

from piekit.managers.structs import AllPlugins
from piekit.system.exceptions import PieException


def on_plugin_available(
    func: Callable = None,
    target: Optional[str] = None
) -> Callable:
    """
    Method decorator used to handle plugin availability

    The methods that use this decorator must have the following signature:
    * `def method(self)` when observing a single plugin
    * `def method(self, target): ...` when observing multiple plugins or all plugins that were listed as dependencies

    Args
        func (callable): Method to decorate. Given by default when applying the decorator
        target(Optional[str]): Name of the requested plugins whose availability triggers the method

    Returns
        func(callable): The same method that was given as input.
    """
    if func is None:
        return functools.partial(on_plugin_available, target=target)

    if target is None:
        # Use special `AllPlugins` identifier to signal that the function
        # observes all plugins listed as dependencies.
        target = AllPlugins

    func._plugin_listen = target
    return func


def on_plugin_unmount(func: Callable = None, target: Optional[str] = None):
    """
    Method decorator used to handle plugins unmount on Spyder.

    This decorator will be called **before** the specified plugins is deleted
    and also **before** the plugins that uses the decorator is destroyed.

    The methods that use this decorator must have the following signature:
    * `def method(self)` when observing a single plugin

    Args
        func (callable): Method to decorate. Given by default when applying the decorator
        target(Optional[str]): Name of the requested plugins whose availability triggers the method

    Returns
        func(callable): The same method that was given as input.
    """
    if func is None:
        return functools.partial(on_plugin_unmount, plugin=target)

    if target is None:
        raise PieException(
            "A method `on_plugin_unmount` must have a well "
            "defined plugins keyword argument value. "
            "For example - target=Container.Workbench"
        )

    func._object_unmount = target
    return func


onPluginAvailable = on_plugin_available
onPluginUnmount = on_plugin_unmount

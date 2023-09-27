import functools
from typing import Callable, Optional

from piekit.managers.structs import AllPlugins
from piekit.exceptions import PieException


def on_plugin_event(func: Callable = None, target: str = None, event: str = None) -> Callable:
    """
    Method decorator used to handle emited plugins' signals
    To use this decorator you need to define a signal in the plugin and emit it manually

    The methods that use this decorator must have the following signature:
        * `def method(self, target, event): ...` when observing multiple plugins or all plugins that were listed as dependencies

    Args:
        * func (callable): Method to decorate. Given by default when applying the decorator
        * target (Optional[str]): Name of the requested plugins whose availability triggers the method
        * event (str): Name of the signal without `sig_` prefix

    Returns:
        * func(callable): The same method that was given as input.
    """
    if not event:
        event = "sig_plugin_ready"
        
    if func is None:
        return functools.partial(on_plugin_event, target=target, event=event)

    func.event_listen = {"target": target, "signal": f"sig_public_{event}"}
    return func


def on_plugin_available(func: Callable = None, target: Optional[str] = None) -> Callable:
    """
    Method decorator used to handle plugin availability

    The methods that use this decorator must have the following signature:
        * `def method(self)` when observing a single plugin
        * `def method(self, target): ...` when observing multiple plugins or all plugins that were listed as dependencies

    Args:
        * func (callable): Method to decorate. Given by default when applying the decorator
        * target (Optional[str]): Name of the requested plugins whose availability triggers the method

    Returns:
        * func (callable): The same method that was given as input.
    """
    if func is None:
        return functools.partial(on_plugin_available, target=target)

    if target is None:
        # Use special `AllPlugins` identifier to signal that the function
        # observes all plugins listed as dependencies.
        target = AllPlugins

    func.plugin_listen = target
    return func


def on_plugin_shutdown(func: Callable = None, target: Optional[str] = None):
    """
    Method decorator used to handle plugins shutdown event

    This decorator will be called **before** the specified plugins is deleted
    and also **before** the plugins that uses the decorator is destroyed

    The methods that use this decorator must have the following signature:
        * `def method(self)` when observing a single plugin

    Args:
        * func (callable): Method to decorate. Given by default when applying the decorator
        * target (Optional[str]): Name of the requested plugins whose availability triggers the method

    Returns:
        * func(callable): The same method that was given as input.
    """
    if func is None:
        return functools.partial(on_plugin_shutdown, target=target)

    if target is None:
        raise PieException(
            "A method `on_plugin_shutdown` must have a well "
            "defined plugins keyword argument value. "
            "For example, `target=Plugin.Workbench`"
        )

    func.plugin_shutdown = target
    return func


onPluginAvailable = on_plugin_available
onPluginShutdown = on_plugin_shutdown

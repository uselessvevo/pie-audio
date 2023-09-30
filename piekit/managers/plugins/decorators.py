import functools
from typing import Callable, Optional


def on_plugin_event(func: Callable = None, target: str = None, event: str = None) -> Callable:
    """
    Method decorator used to handle emitted plugins' signals
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
        event = "plugin_ready"
        
    if func is None:
        return functools.partial(on_plugin_event, target=target, event=event)

    func.event_listen = {"target": target, "event": event, "signal": f"sig_{event}"}
    return func

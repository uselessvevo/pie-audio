import functools
from typing import Callable, Optional

from piekit.managers.types import AllPieObjects


def on_object_available(
    func: Callable = None,
    target: Optional[str] = None
) -> Callable:
    """
    Method decorator used to handle PieObject availability

    The methods that use this decorator must have the following signature:
    `def method(self)` when observing a single pie_object or
    `def method(self, target): ...` when observing multiple pie_objects or
    all PieObjects that were listed as dependencies.

    Parameters
    ----------
    func: Callable
        Method to decorate. Given by default when applying the decorator.
    target: Optional[str]
        Name of the requested PieObjects whose availability triggers the method.

    Returns
    -------
    func: Callable
        The same method that was given as input.
    """
    if func is None:
        return functools.partial(on_object_available, target=target)

    if target is None:
        # Use special `AllPieObjects` identifier to signal that the function
        # observes all PieObjects listed as dependencies.
        target = AllPieObjects

    func._object_listen = target
    return func


def on_object_unmount(func: Callable = None, target: Optional[str] = None):
    """
    Method decorator used to handle PieObjects unmount on Spyder.

    This decorator will be called **before** the specified PieObjects is deleted
    and also **before** the PieObjects that uses the decorator is destroyed.

    The methods that use this decorator must have the following signature:
    `def method(self)`.

    Parameters
    ----------
    func: Callable
        Method to decorate. Given by default when applying the decorator.
    target: str
        Name of the requested PieObjects whose unmount triggers the method.

    Returns
    -------
    func: Callable
        The same method that was given as input.
    """
    if func is None:
        return functools.partial(on_object_unmount, plugin=target)

    if target is None:
        raise ValueError("on_object_unmount must have a well defined "
                         "PieObjects keyword argument value, "
                         "e.g., target=Objects.Editor")

    func._object_unmount = target
    return func


onObjectAvailable = on_object_available
onPieObjectUnmount = on_object_unmount

import abc
from typing import TypeVar, Protocol, Generic, Callable, Any

# TODO: Add Expandable types mixing. For example: `EList[EDict, ...]`

__all__ = (
    "elist",
    "edict"
)


TCallable = TypeVar("TCallable", bound=Callable[..., Any], covariant=True)


class etype(Protocol(Generic[TCallable])):
    """ Expandable type """

    @abc.abstractmethod
    def __call__(self, previous_value: Any, value: Any) -> Any:
        pass


class elist(etype):
    """ Expandable list """

    def __call__(self, previous_value: Any, value: Any) -> Any:
        previous_value.extend(value)
        return previous_value


class edict(etype):
    """ Expandable dictionary """

    def __call__(self, previous_value: Any, value: Any) -> Any:
        previous_value.update(**value)
        return previous_value

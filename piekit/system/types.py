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

    def __init__(self, frozen: bool = False) -> None:
        self._frozen = frozen

    @property
    def frozen(self) -> bool:
        return self._frozen

    @abc.abstractmethod
    def __call__(self, previous_value: Any, new_value: Any) -> Any:
        """
        Use this method to handle new value and extend the previous one
        
        Args:
            previous_value (Any): previous value that will be expanded
            new_value (Any): new value that will be used to expand `previous_value`

        Returns:
            previous_value (Any):
        """


class elist(etype):
    """ Expandable list """

    def __call__(self, previous_value: Any, new_value: Any) -> Any:
        previous_value.extend(new_value)
        return previous_value


class edict(etype):
    """ Expandable dictionary """

    def __call__(self, previous_value: Any, new_value: Any) -> Any:
        previous_value.update(**new_value)
        return previous_value

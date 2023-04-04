import abc
from typing import Any

# TODO: Add Expandable types mixing. For example: `EList[EDict, ...]`

__all__ = (
    "EList",
    "EDict"
)


class EType:
    """ Expandable type """

    @abc.abstractmethod
    def __call__(self, previous_value: Any, value: Any) -> Any:
        pass


class EList(EType):
    """ Expandable list """
    def __call__(self, previous_value: Any, value: Any) -> Any:
        previous_value.extend(value)
        return previous_value


class EDict(EType):
    """ Expandable dictionary """

    def __call__(self, previous_value: Any, value: Any) -> Any:
        previous_value.update(**value)
        return previous_value

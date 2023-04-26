import abc
from typing import Any


__all__ = ("Lock",)


class Annotated(abc.ABC):
    """
    All implementations must contain private `attributes <dict[str, Any]>` field
    """

    @abc.abstractmethod
    def set(self, field: str, value: Any) -> Any:
        pass

    @abc.abstractmethod
    def get(self, field: str) -> Any:
        pass

    @property
    @abc.abstractmethod
    def attributes(self) -> dict[str, Any]:
        pass


class Lock(Annotated):

    def __init__(self) -> None:
        self.__attributes: dict[str, Any] = {}

    def set(self, field: str, value: Any) -> Any:
        if field in self.__attributes:
            raise KeyError(f"{field} is locked - you can't change its value")
            
        self.__attributes[field] = value

    def get(self, field: str) -> Any:
        return self.__attributes.get(field)

    @property
    def attributes(self) -> dict[str, Any]:
        return self.__attributes

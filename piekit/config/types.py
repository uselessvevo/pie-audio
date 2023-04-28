import abc
from typing import Any


__all__ = ("Lock", "Max")


class AnnotatedHandler:
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


class LockHandler(AnnotatedHandler):

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


class MaxHandler(AnnotatedHandler):

    def __init__(self) -> None:
        self.__attributes: dict[str, Any] = {}

    def set(self, field: str, value: Any) -> Any:
        if len(value) > self.__max:
            raise ValueError(f"Field {field} bigger than max value ({self.__max})")

        self.__attributes[field] = value

    def get(self, field: str) -> Any:
        return self.__attributes[field]

    def __class_getitem__(cls, max_value: int) -> None:
        if not isinstance(max_value, int):
            raise TypeError("Max value must be integer")

        cls.__max = max_value

    @property
    def attributes(self) -> dict[str, Any]:
        return self.__attributes


class LenHandler(AnnotatedHandler):

    def __init__(self) -> None:
        self.__attributes: dict[str, Any] = {}

    def set(self, field: str, value: Any) -> Any:
        if len(value) < self.__max:
            raise ValueError(f"Field {field} is smaller than min value ({self.__min})")

        self.__attributes[field] = value

    def get(self, field: str) -> Any:
        return self.__attributes[field]

    def __class_getitem__(cls, min_value: int) -> None:
        if not isinstance(min_value, int):
            raise TypeError("Min value must be integer")

        cls.__min = min_value

    @property
    def attributes(self) -> dict[str, Any]:
        return self.__attributes


Max = type("Max", (MaxHandler,), {})
Min = type("Min", (LenHandler,), {})
Lock = type("Lock", (LockHandler,), {})

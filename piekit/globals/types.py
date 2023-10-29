from __future__ import annotations

import inspect
import sys
from typing import Any, Type


class AnnotatedHandler:

    def set(self, field: str, value: Any) -> Any:
        raise NotImplementedError("Method \"set\" must be implemented")

    def get(self, field: str) -> Any:
        raise NotImplementedError("Method \"get\" must be implemented")


class LockHandler(AnnotatedHandler):

    def __init__(self) -> None:
        self.__attributes: dict[str, Any] = {}

    def set(self, field: str, value: Any) -> Any:
        if field in self.__attributes:
            raise KeyError(f"{field} is locked - you can't change its value")
            
        self.__attributes[field] = value

    def get(self, field: str) -> Any:
        return self.__attributes.get(field)


class MaxHandler(AnnotatedHandler):

    def __init__(self) -> None:
        self.__attributes: dict[str, Any] = {}

    def set(self, field: str, value: Any) -> Any:
        if len(value) > self.__max:
            raise ValueError(f"Field {field} bigger than max value ({self.__max})")

        self.__attributes[field] = value

    def get(self, field: str) -> Any:
        return self.__attributes[field]

    def __class_getitem__(cls, max_value: int) -> Type[MaxHandler]:
        if not isinstance(max_value, int):
            raise TypeError("Max value must be integer")

        cls.__max = max_value
        return cls


class MinHandler(AnnotatedHandler):

    def __init__(self) -> None:
        self.__attributes: dict[str, Any] = {}

    def set(self, field: str, value: Any) -> Any:
        if len(value) < self.__min:
            raise ValueError(f"Field {field} is smaller than min value ({self.__min})")

        self.__attributes[field] = value

    def get(self, field: str) -> Any:
        return self.__attributes[field]

    def __class_getitem__(cls, min_value: int) -> Type[MinHandler]:
        if not isinstance(min_value, int):
            raise TypeError("Min value must be integer")

        cls.__min = min_value
        return cls


# Define these aliases to ignore linter errors
Max = type("Max", (MaxHandler,), {})
Min = type("Min", (MinHandler,), {})
Lock = type("Lock", (LockHandler,), {})


__all__ = list(i[0] for i in inspect.getmembers(sys.modules[__name__], inspect.isclass) if not i[0].endswith("Handler"))

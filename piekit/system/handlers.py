import abc
from typing import Any 


class IHandler:

    __slots__ = ()

    @abc.abstractmethod
    def __call__(self, pre_value: Any, value: Any) -> Any:
        pass


class EListHandler(IHandler):

    def __call__(self, pre_value: Any, value: Any) -> Any:
        pre_value.extend(value)
        return pre_value


class EDictHandler(IHandler):

    def __call__(self, pre_value: Any, value: Any) -> Any:
        pre_value.update(**value)
        return pre_value

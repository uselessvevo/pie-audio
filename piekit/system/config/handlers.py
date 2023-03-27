import abc
from typing import Any 


class IHandler:

    __slots__ = ()

    @abc.abstractmethod
    def handle(self, value: Any) -> Any:
        pass



class EListHandler(IHandler):

    def handle(self, value: Any) -> Any:
        new_value = value
        new_value.extend(value)
        return new_value


class EDictHandler(IHandler):

    def handle(self, value: Any) -> Any:
        new_value = value
        new_value.update(**value)
        return new_value

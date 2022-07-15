import abc
from typing import Any


class IManager(abc.ABC):
    name: str

    def init(self, *args, **kwargs) -> None:
        """ Main entrypoint. Call it before `mount` method """

    def destroy(self, *args, **kwargs) -> None:
        """ Main entrypoint for quiting """

    @abc.abstractmethod
    def mount(self, parent=None) -> None:
        """ Method for objects registration """

    @abc.abstractmethod
    def unmount(self, parent=None) -> None:
        """ Method for objects deregistration """

    def set(self, key, *args, **kwargs) -> None:
        """ Set data by key """

    def get(self, key, default: Any = None) -> Any:
        """ Get data by key """

    def delete(self, key) -> None:
        """ Delete data by key """

    def reload(self, *args, **kwargs) -> None:
        """ Reload manager """

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {id(self)}>'

import abc
from typing import Any


class IManager(abc.ABC):
    name: str

    @abc.abstractmethod
    def mount(self) -> None:
        """ Mount managers, services. A good example is `Plugin/GenericPlugin` """

    def unmount(self, *args, **kwargs) -> None:
        """ Method for object deregistration """

    def set(self, key, *args, **kwargs) -> None:
        """ Set data by key """

    def get(self, key, default: Any = None) -> Any:
        """ Get data by key """

    def delete(self, key) -> None:
        """ Delete data by key """

    def reload(self, *args, **kwargs) -> None:
        """ Reload manager """

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {id(self)}>'

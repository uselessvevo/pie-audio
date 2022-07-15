import abc

from PyQt5.QtCore import QObject


class IComponent(QObject, abc.ABC):
    name: str

    @abc.abstractmethod
    def init(self):
        pass

    def mount(self):
        pass

    def unmount(self):
        pass

    def reload(self, *args, **kwargs):
        pass

    def destroy(self):
        pass

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {id(self)}>'

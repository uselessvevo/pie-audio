import abc


class IComponent(abc.ABC):

    @abc.abstractmethod
    def mount(self):
        pass

    @abc.abstractmethod
    def reload(self):
        pass

    @abc.abstractmethod
    def destroy(self):
        pass

    def __str__(self) -> str:
        return self.__class__.__name__

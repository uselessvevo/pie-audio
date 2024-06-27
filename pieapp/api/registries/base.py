from typing import Any


class BaseRegistry:
    name: str

    def init(self, *args, **kwargs) -> None:
        """
        Optional initializer
        """

    def shutdown(self):
        """
        This method serves to reset all containers, variables etc.
        Don't use it to delete data from memory
        """

    def reload(self):
        """
        This method reload manager
        """
        self.shutdown()
        self.init()

    def add(self, *args, **kwargs) -> None:
        pass

    def get(self, *args, **kwargs) -> Any:
        pass

    def update(self, *args, **kwargs) -> None:
        pass

    def items(self, *args, **kwargs) -> list[Any]:
        pass

    def values(self, *args, **kwargs) -> list[Any]:
        pass

    def remove(self, *args, **kwargs) -> None:
        pass

    def restore(self, *args, **kwargs) -> None:
        pass

    def contains(self, *args, **kwargs) -> bool:
        pass

    def index(self, *args, **kwargs) -> int:
        pass

    def __getitem__(self, *args, **kwargs) -> Any:
        return self.get(*args, **kwargs)

    def __contains__(self, *args, **kwargs) -> Any:
        return self.contains(*args, **kwargs)

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <name: {self.name}>"

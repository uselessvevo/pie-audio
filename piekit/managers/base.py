from typing import Any

from piekit.utils.logger import logger


class BaseManager:
    # Manager name
    name: str

    # Contains a tuple of required `BaseManager` based objects name
    dependencies: tuple[str] = None

    def __init__(self) -> None:
        # Just a logger
        self._logger = logger

        # Is manager ready
        self._ready: bool = False

    def init(self, *args, **kwargs) -> None:
        """
        Optional initializer
        """

    def shutdown(self, *args, **kwargs):
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

    def set(self, *args, **kwargs) -> None:
        """
        Set data by key
        Arguments example: `key: Any, data: Any`
        """

    def get(self, *args, **kwargs) -> Any:
        """
        Get data by key
        Arguments example: `key: Any, default: Any = None`
        """

    def delete(self, *args, **kwargs) -> None:
        """
        Delete data by key
        Arguments example: `key: Any`
        """

    @property
    def ready(self) -> bool:
        return self._ready

    @ready.setter
    def ready(self, ready: bool) -> None:
        self._ready = ready

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {id(self)}>'

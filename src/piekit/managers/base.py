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

        # Is manager mounted
        self._mounted: bool = False

    def mount(self, *args, **kwargs) -> None:
        raise NotImplementedError("Method `mount` must be implemented")

    def unmount(self, *args, **kwargs):
        """
        This method serves to reset all containers, variables etc.
        Don't use it to delete data from memory
        """

    def reload(self):
        """
        This method reload manager
        """

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
    def mounted(self) -> bool:
        return self._mounted

    @mounted.setter
    def mounted(self, mounted: bool) -> None:
        self._mounted = mounted

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {id(self)}>'

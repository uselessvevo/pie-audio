from typing import Any
from PyQt5.QtCore import QObject

from cloudykit.objects.logger import logger


class BaseManager(QObject):
    # Contains a tuple of required `BaseManager` based objects name
    dependencies: tuple[str] = None

    def __init__(self, parent: "SystemManager") -> None:
        super().__init__(parent)

        # By default, parent attribute can (or must) be a `SystemManager` object
        self._parent: "SystemManager" = parent

        # Just a logger
        self._logger = logger

        # Is manager mounted
        self._mounted: bool = False

    def mount(self) -> None:
        raise NotImplementedError("Method `mount` must be implemented")

    def unmount(self):
        pass

    def set(self, key: Any, data: Any) -> None:
        """ Set data by key """
        pass

    def get(self, key: Any, default: Any = None) -> Any:
        """ Get data by key """
        pass

    def delete(self, key: Any) -> None:
        """ Delete data by key """
        pass

    @property
    def parent(self) -> "SystemManager":
        return self._parent

    @property
    def registry(self) -> "ManagerRegistry":
        return self._parent.registry

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

from typing import Any, Union

from piekit.plugins.plugins import PiePlugin
from piekit.plugins.api.exceptions import ApiMethodNotFoundError


class PiePluginAPI:

    def __init__(self, parent: Union[None, PiePlugin] = None) -> None:
        self._parent = parent

    def mount(self) -> None:
        pass

    def __call__(self, method: str, **kwargs) -> Any:
        try:
            return self.__getattribute__(method)(**kwargs)
        except AttributeError:
            raise ApiMethodNotFoundError(method)

    @property
    def parent(self) -> PiePlugin:
        return self._parent

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}> (id: {id(self)}, parent: {self._parent})"

"""
API exceptions
"""


class NoApiImplementationError(AttributeError):

    def __init__(self, plugin: str) -> None:
        self._method = plugin

    def __str__(self) -> str:
        return f"Method {self._method} not found"


class ApiMethodNotFoundError(AttributeError):

    def __init__(self, method: str) -> None:
        self._method = method

    def __str__(self) -> str:
        return f"Method {self._method} not found"

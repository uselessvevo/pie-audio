"""
API exceptions
"""


class ApiMethodNotFoundError(AttributeError):

    def __init__(self, method: str) -> None:
        self._method = method

    def __str__(self) -> str:
        return f"Method {self._method} not found"

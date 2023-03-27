"""
System exceptions
"""


class PieException(Exception):
    pass


class HandlerNotFoundError(Exception):

    def __init__(self, name: str) -> None:
        self._name = name

    def __str__(self) -> str:
        return f"Handler {self._name} not found"


class HandlerNotImportedError(Exception):

    def __init__(self, name: str) -> None:
        self._name = name

    def __str__(self) -> str:
        return f"Handler {self._name} not imported"

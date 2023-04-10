"""
Exceptions
"""


class DependencyNotFoundError(AttributeError):

    def __init__(self, name: str) -> None:
        self._name = name

    def __str__(self):
        return f"Required manager {self._name} not found"


class ManagerNotReadyError(AttributeError):

    def __init__(self, name: str) -> None:
        self._name = name

    def __str__(self):
        return f"Manager {self._name} not ready"

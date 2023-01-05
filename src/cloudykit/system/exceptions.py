class DependencyNotFoundError(AttributeError):

    def __init__(self, name: str) -> None:
        self._name = name

    def __str__(self):
        return f"Required manager {self._name} not found"


class ObjectNotMountedError(AttributeError):

    def __init__(self, name: str) -> None:
        self._name = name

    def __str__(self):
        return f"Object {self._name} not mounted"

"""
System exceptions
"""
from pieapp.api.registries.locales.helpers import translate


class PieError(Exception):
    error_type: str = "default"

    def __init__(
        self,
        title: str = None,
        description: str = None,
        raise_exception: bool = False
    ) -> None:
        self._title = translate(title or "Error")
        self._description = translate(description or "An error has been occurred")
        self._raise_exception = raise_exception

    def as_dict(self) -> dict:
        return {
            "title": self._title,
            "description": self._description,
            "raise_exception": self._raise_exception
        }

    def __str__(self) -> str:
        return f"{self._title} - {self._description}"


class NotificationError(PieError):
    error_type = "info"

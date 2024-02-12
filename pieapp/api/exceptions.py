"""
System exceptions
"""
from pieapp.api.managers.locales.helpers import translate


class PieException(Exception):

    def __init__(
        self,
        title: str = None,
        description: str = None,
        code: int = None,
        raise_exception: bool = False
    ) -> None:
        self._code = code
        self._title = translate(title or "Error")
        self._description = translate(description or "An error has been occurred")
        self._raise_exception = raise_exception

    def get_dict(self) -> dict:
        return {
            "code": self._code,
            "title": self._title,
            "description": self._description,
            "raise_exception": self._raise_exception
        }

    def __str__(self) -> str:
        return f"{self._title}[{self._code}] - {self._description}"

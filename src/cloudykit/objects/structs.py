import dataclasses as dt


@dt.dataclass
class Error:
    title: str
    code: str = dt.field(default="error")
    description: str = dt.field(default="Some error has been occurred")
    exception: Exception = dt.field(default_factory=Exception)
    raise_error: bool = dt.field(default=False)

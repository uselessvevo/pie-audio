import dataclasses as dt


SharedSection = "shared"

AllPieObjects = "__ALL__"

# Use it in `AssetsManager`
DirectoryType = type("DirectoryType", (), {})


@dt.dataclass
class Error:
    title: str
    code: str = dt.field(default="error")
    description: str = dt.field(default="Some error has been occurred")
    exception: Exception = dt.field(default_factory=Exception)
    raise_error: bool = dt.field(default=False)

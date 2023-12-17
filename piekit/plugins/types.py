from enum import Enum
import dataclasses as dt


class PluginType(Enum):
    # Plugin
    Plugin: str = "plugin"

    # Object
    Object: str = "manager"


@dt.dataclass
class Error:
    title: str
    code: str = dt.field(default="error")
    description: str = dt.field(default="Some error has been occurred")
    exception: Exception = dt.field(default_factory=Exception)
    raise_error: bool = dt.field(default=False)

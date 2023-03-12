import dataclasses as dt


class PluginTypes:
    # Plugin
    Plugin: str = "plugin"

    # Container
    Container: str = "container"


@dt.dataclass
class Error:
    title: str
    code: str = dt.field(default="error")
    description: str = dt.field(default="Some error has been occurred")
    exception: Exception = dt.field(default_factory=Exception)
    raise_error: bool = dt.field(default=False)

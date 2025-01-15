import dataclasses as dt


@dt.dataclass(init=False, frozen=True, eq=False)
class PluginType:
    Object: str = "object"
    Plugin: str = "plugin"
    Manager: str = "manager"

    @classmethod
    def fields(cls) -> list[str]:
        return [i.default for i in dt.fields(cls)]


@dt.dataclass(eq=True, slots=True)
class Error:
    title: str
    code: str = dt.field(default="error")
    description: str = dt.field(default="Some error has been occurred")
    exception: Exception = dt.field(default_factory=Exception)
    raise_error: bool = dt.field(default=False)

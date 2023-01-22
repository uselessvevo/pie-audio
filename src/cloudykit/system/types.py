import typing
import dataclasses as dt

# TODO: Add Expandable types mixing. For example: `EList[EDict, ...]`

# Expandable list
from pathlib import Path

EList = typing.TypeVar("EList")

# Expandable dict
EDict = typing.TypeVar("EDict")

# Use it in `AssetsManager`
DirectoryType = type("DirectoryType", (), {})


@dt.dataclass(frozen=True, eq=False)
class ManagerConfig:
    import_string: typing.Optional[str]
    mount: bool = dt.field(default=False)
    args: tuple = dt.field(default_factory=tuple)
    kwargs: dict = dt.field(default_factory=dict)


@dt.dataclass(frozen=True, eq=False)
class PathConfig:
    root: Path
    section: str = dt.field(default=None)
    section_stem: bool = dt.field(default=True)
    pattern: str = dt.field(default=".json")

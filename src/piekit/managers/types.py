"""
Default managers
"""
import typing
import dataclasses as dt
from pathlib import Path


class SysManagers:
    # ConfigManager
    Configs = "configs"
    
    # LocaleManager
    Locales = "locales"
    
    # AssetsManager
    Assets = "assets"

    # ShortcutsManager
    Shortcuts = "shortcuts"

    # ObjectManager
    Objects = "objects"


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
    section_stem: bool = dt.field(default=False)
    pattern: str = dt.field(default="*.json")


SharedSection = "shared"
AllPieObjects = "__ALL__"
DirectoryType = type("DirectoryType", (), {})

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

    # PluginManager
    Plugins = "plugins"
    
    # MenuManager
    Menus = "menus"

    # ToolButtonManager
    ToolButton = "toolbuttons"

    # ToolBarManager
    ToolBars = "toolbar"

    # ActionManager
    Actions = "actions"
    

class Sections:
    # User/site access section
    User = "user"
    
    # Shared/root access section
    Shared = "shared"


@dt.dataclass(frozen=True, eq=False)
class ManagerConfig:
    import_string: typing.Optional[str]
    mount: bool = dt.field(default=False)
    args: tuple = dt.field(default_factory=tuple)
    kwargs: dict = dt.field(default_factory=dict)


AllPlugins = "__ALL__"
DirectoryType = type("DirectoryType", (), {})
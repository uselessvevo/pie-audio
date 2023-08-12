"""
Default managers
"""
from typing import Optional, Union
import dataclasses as dt


class SysManager:
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

    # ConfigPageManager
    ConfigPages = "configpages"

    # LayoutManager
    Layouts = "layouts"
    

class Section:
    """
    Configuration categories/sections
    """

    # Application/root scope
    Root = "root"
    
    # Plugin section name
    Inner = "inner"

    # User/third-party section name
    User = "user"
    
    # Shared access section
    Shared = "shared"


@dt.dataclass(frozen=True, eq=False)
class ManagerConfig:
    import_string: Optional[str]
    init: bool = dt.field(default=False)
    args: tuple = dt.field(default_factory=tuple)
    kwargs: dict = dt.field(default_factory=dict)


AllPlugins = "__ALL__"
DirectoryType = type("DirectoryType", (), {})

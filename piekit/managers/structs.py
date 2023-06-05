"""
Default managers
"""
import typing
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

    # ConfigurationPageManager
    ConfigPages = "configpages"
    

class Section:
    """
    Configuration categories/sections
    """

    # Application/root scope
    Root = "root"
    
    # Plugin section name
    Inner = "inner"

    # User/site section name
    User = "user"
    
    # Shared access section
    # TODO: Remove it in the future releases
    Shared = "shared"


@dt.dataclass(frozen=True, eq=False)
class ManagerConfig:
    import_string: typing.Optional[str]
    init: bool = dt.field(default=False)
    args: tuple = dt.field(default_factory=tuple)
    kwargs: dict = dt.field(default_factory=dict)


AllPlugins = "__ALL__"
DirectoryType = type("DirectoryType", (), {})

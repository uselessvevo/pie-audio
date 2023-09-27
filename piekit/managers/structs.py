"""
Default managers
"""


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


AllPlugins = "__ALL__"
DirectoryType = type("DirectoryType", (), {})

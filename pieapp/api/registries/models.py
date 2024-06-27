"""
Default Registrys
"""


class SysRegistry:
    # ConfigRegistry
    Configs = "configs"
    
    # LocaleRegistry
    Locales = "locales"
    
    # AssetsRegistry
    Themes = "assets"

    # IconsRegistry
    Icons = "icons"

    # ShortcutsRegistry
    Shortcuts = "shortcuts"

    # PluginRegistry
    Plugins = "plugins"
    
    # MenuRegistry
    Menus = "menus"

    # ToolButtonRegistry
    ToolButton = "toolbuttons"

    # ToolBarRegistry
    ToolBars = "toolbar"

    # ActionRegistry
    Actions = "actions"

    # ConfigPageRegistry
    ConfigPages = "configpages"

    # LayoutRegistry
    Layout = "layout"

    # FileSnapshotRegistry
    Snapshots = "snapshots"
    

class Scope:
    """
    Configuration categories/sections
    """

    # Application/root scope
    Root = "root"
    
    # Plugin scope name
    Inner = "inner"

    # User/third-party scope name
    User = "user"
    
    # Shared access scope
    Shared = "shared"


AllPlugins = "__ALL__"

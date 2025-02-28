"""
Built-in layouts
"""


class Layout:
    # Tools layout is used to display tool widgets.
    # For example: toolbar, additional menus, etc.
    # Uses `QVBoxLayout`
    # P.S: Menus from `MainWindow` are not registered on this layout
    Tools = "tools"

    # Canvas layout is used to display main widgets
    # For example: converter's list widget
    # Uses `QGridLayout`
    Workspace = "workspace"
    WorkspaceCenter = "workspace-center"
    WorkspaceRight = "workspace-right"
    WorkspaceBottom = "workspace-bottom"

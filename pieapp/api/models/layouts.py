"""
Built-in layouts
"""


class Layout:
    # Tools layout is used to display tool widgets.
    # For example: toolbar, additional menus, etc.
    # Uses `QHBoxLayout`
    # P.S: Menus from `MainWindow` are not registered on this layout
    Tools = "tools"

    # Canvas layout is used to display main widgets
    # For example: converter's list widget
    # Uses `QGridLayout`
    Main = "main"

    # Info layout is used to display information
    # For example: status bar, etc.
    # Uses `QHBoxLayout`
    Info = "info"

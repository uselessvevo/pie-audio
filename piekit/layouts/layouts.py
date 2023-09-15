from __future__ import annotations

from piekit.globals import Global
from piekit.layouts.structs import Layout


class BaseLayout:
    name: str


class MainGridLayout(BaseLayout, Global.MAIN_GRID_LAYOUT_CLASS):
    """ Use this class as the root layout for all widgets, layouts, etc."""
    name = Layout.Main

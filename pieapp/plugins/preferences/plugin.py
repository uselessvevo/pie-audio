from __feature__ import snake_case

from typing import Union

from PySide6.QtGui import Qt
from PySide6.QtCore import Slot

from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTreeWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QDialogButtonBox

from pieapp.api.managers.locales.helpers import translate
from pieapp.api.structs.plugins import Plugin
from pieapp.api.structs.menus import MainMenu
from pieapp.api.structs.menus import MainMenuItem

from pieapp.api.globals import Global
from pieapp.api.plugins.confpage import ConfigPage

from pieapp.widgets.spacer import Spacer
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.managers.structs import Section
from pieapp.api.plugins.decorators import on_plugin_event
from pieapp.api.managers.menus.mixins import MenuAccessorMixin
from pieapp.api.managers.themes.mixins import ThemeAccessorMixin
from pieapp.api.managers.configs.mixins import ConfigAccessorMixin
from pieapp.api.managers.toolbars.mixins import ToolBarAccessorMixin
from pieapp.api.managers.toolbuttons.mixins import ToolButtonAccessorMixin

from preferences.widgets.item import ConfigPageTreeWidget


ConfigPagesDict = dict[str, dict]
ConfigPagesList = list[dict[str, ConfigPage]]
ConfigPagesUnion = Union[ConfigPagesList, ConfigPagesDict]


class Preferences(
    PiePlugin,
    ConfigAccessorMixin, ThemeAccessorMixin,
    MenuAccessorMixin, ToolBarAccessorMixin, ToolButtonAccessorMixin,
):
    name = Plugin.Preferences
    requires = [Plugin.MainMenuBar]

    def __init__(self, *args, **kwargs) -> None:
        super(Preferences, self).__init__(*args, **kwargs)

        # Define main container variables
        self._pages_dict: dict[str, ConfigPage] = {}
        self._tree_item_dict: dict[str, ConfigPageTreeWidget] = {}

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg", section=self.name)

    def init(self) -> None:
        # Main window dialog
        self._dialog = QDialog(self._parent)
        self._dialog.set_modal(True)
        self._dialog.set_object_name("PreferencesDialog")
        self._dialog.set_window_title(translate("Preferences"))
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.set_minimum_size(*Global.DEFAULT_MIN_WINDOW_SIZE)
        self._dialog.resize(*self.get_config("ui.window_size", Global.DEFAULT_MIN_WINDOW_SIZE))

        # Page canvas and its state
        self._page_widget_grid = QGridLayout()
        self._page_widget_grid.set_contents_margins(0, 0, 0, 0)

        self._current_canvas_widget = QLabel()
        self._current_canvas_widget.set_object_name("PreferencesCurrentWidget")
        self._current_canvas_widget.set_alignment(Qt.AlignmentFlag.AlignCenter)

        # Footer layout
        self._command_buttons_footer_grid = QGridLayout()
        self._command_buttons_footer_grid.set_horizontal_spacing(0)
        self._command_buttons_footer_grid.set_contents_margins(0, 0, 0, 0)

        self._footer_button_box = QDialogButtonBox()
        self._footer_button_box.set_contents_margins(0, 10, 10, 10)

        self._ok_button = QPushButton()
        self._ok_button.set_text(translate("Ok"))
        self._ok_button.clicked.connect(self._on_pages_accept)

        self._cancel_button = QPushButton()
        self._cancel_button.set_text(translate("Cancel"))
        self._cancel_button.clicked.connect(self._on_pages_cancel)

        self._apply_button = QPushButton()
        self._apply_button.set_text(translate("Apply"))
        self._apply_button.set_enabled(False)
        self._apply_button.clicked.connect(self._on_pages_apply)

        self._footer_button_box.add_button(self._ok_button, QDialogButtonBox.ButtonRole.AcceptRole)
        self._footer_button_box.add_button(self._cancel_button, QDialogButtonBox.ButtonRole.RejectRole)
        self._footer_button_box.add_button(self._apply_button, QDialogButtonBox.ButtonRole.ApplyRole)

        # Connect standard buttons

        self._ok_button.clicked.connect(self._on_pages_accept)
        self._cancel_button.clicked.connect(self._on_pages_cancel)
        self._apply_button.set_enabled(False)
        self._apply_button.clicked.connect(self._on_pages_apply)

        self._command_buttons_footer_grid.add_widget(Spacer(), 0, 0, Qt.AlignmentFlag.AlignRight)
        self._command_buttons_footer_grid.add_widget(self._footer_button_box, 0, 1, Qt.AlignmentFlag.AlignRight)

        self._page_widget_grid.add_widget(self._current_canvas_widget, 0, 0)

        # Tree widget
        self._tree_widget = QTreeWidget()
        self._tree_widget.set_header_hidden(True)
        self._tree_widget.set_indentation(0)
        self._tree_widget.set_object_name("PreferencesTreeWidget")
        self._tree_widget.itemClicked.connect(self._on_item_clicked)

        self._root_grid = QGridLayout(self._dialog)
        self._root_grid.add_widget(self._tree_widget, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self._root_grid.add_layout(self._page_widget_grid, 0, 1, Qt.AlignmentFlag.AlignTop)
        self._root_grid.add_widget(Spacer(), 1, 0, Qt.AlignmentFlag.AlignBottom)
        self._root_grid.add_layout(self._command_buttons_footer_grid, 2, 0, 10, 0)

        self._dialog.set_layout(self._root_grid)

    def call(self) -> None:
        self._dialog.show()

    # Public API methods

    def register_config_page(self, plugin_instance: PiePlugin) -> None:
        plugin_config_page = getattr(plugin_instance, "get_config_page")
        if plugin_config_page and callable(plugin_config_page):
            config_page_instance: ConfigPage = plugin_config_page()
            self._pages_dict[plugin_instance.name] = config_page_instance

            config_page_instance.init()
            config_page_instance.sig_enable_apply_button.connect(
                lambda: self._enable_apply_button(config_page_instance.is_modified)
            )

            tree_item = ConfigPageTreeWidget(config_page_instance)
            if config_page_instance.get_icon():
                tree_item.set_icon(0, config_page_instance.get_icon())
                tree_item.set_text(1, config_page_instance.get_title())

            tree_item.set_text(0, config_page_instance.get_title())
            self._tree_item_dict[tree_item.confpage.name] = tree_item
            self._tree_widget.add_top_level_item(tree_item)

    def deregister_config_page(self, plugin_instance: PiePlugin) -> None:
        if plugin_instance.name in self._pages_dict:
            self._pages_dict.pop(plugin_instance.name)
            for index, tree_item in enumerate(self._tree_item_dict.values()):
                if tree_item.confpage.name == plugin_instance.name:
                    self._tree_widget.remove_item_widget(tree_item, index)

    def _enable_apply_button(self, state: bool) -> None:
        self._apply_button.set_enabled(state)

    @Slot(ConfigPageTreeWidget, int)
    def _on_item_clicked(self, page: ConfigPageTreeWidget) -> None:
        """
        Handle on item clicked event by swapping current widget with the new one

        Args:
            page (ConfigPageTreeWidget): configuration page instance
        """
        # This is a retarded way to swap components but that will do
        self._page_widget_grid.remove_widget(self._current_canvas_widget)
        self._current_canvas_widget.set_visible(False)
        self._current_canvas_widget = page.confpage.get_page_widget()
        self._current_canvas_widget.set_size_policy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self._page_widget_grid.add_widget(self._current_canvas_widget, 0, 0)
        self._current_canvas_widget.set_visible(True)

    def _on_pages_accept(self) -> None:
        pages = self._pages_dict.values()
        for page in pages:
            page.accept()

        self._dialog.accept()

    def _on_pages_cancel(self) -> None:
        # TODO: Add changes tracker subscription
        pages = self._pages_dict.values()
        for page in pages:
            page.cancel()

        self._dialog.accept()

    def _on_pages_apply(self) -> None:
        pages = self._pages_dict.values()
        for page in pages:
            page.accept()

    @on_plugin_event(target=Plugin.MainMenuBar)
    def _on_menu_bar_available(self) -> None:
        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name="preferences",
            text=translate("Preferences"),
            triggered=self.call,
            icon=self.get_plugin_icon(),
            before=MainMenuItem.Exit
        )


def main(parent: "QMainWindow", plugin_path: "Path"):
    return Preferences(parent, plugin_path)

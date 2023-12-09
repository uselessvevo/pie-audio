from __feature__ import snake_case

from typing import Union

from PySide6.QtGui import Qt
from PySide6.QtCore import Slot

from piekit.globals import Global
from pieapp.structs.menus import MainMenu
from pieapp.structs.menus import MainMenuItem
from pieapp.structs.plugins import Plugin

from piekit.managers.confpages.mixins import ConfigPageAccessorMixin
from piekit.managers.confpages.structs import CustomTreeWidgetItem, ConfigPage

from piekit.widgets.spacer import Spacer
from piekit.plugins.plugins import PiePlugin
from piekit.managers.structs import Section
from piekit.managers.menus.mixins import MenuAccessorMixin
from piekit.managers.themes.mixins import ThemeAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.managers.toolbars.mixins import ToolBarAccessorMixin
from piekit.managers.toolbuttons.mixins import ToolButtonAccessorMixin
from piekit.managers.plugins.decorators import on_plugin_event

from PySide6.QtWidgets import QGridLayout, QDialog, QTreeWidget, QLabel, QDialogButtonBox, QPushButton


class Settings(
    PiePlugin,
    ConfigPageAccessorMixin,
    ConfigAccessorMixin, LocalesAccessorMixin, ThemeAccessorMixin,
    MenuAccessorMixin, ToolBarAccessorMixin, ToolButtonAccessorMixin,
):
    name = Plugin.Settings
    requires = [Plugin.MenuBar]

    def init(self) -> None:
        # Main window dialog
        self._dialog = QDialog(self._parent)
        self._dialog.set_modal(True)
        self._dialog.set_object_name("SettingsDialog")
        self._dialog.set_window_title(self.translate("Settings"))
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.set_minimum_size(*Global.SETTINGS_PLUGIN_MIN_SIZE)
        self._dialog.resize(*self.get_config("ui.window_size", Global.SETTINGS_PLUGIN_MIN_SIZE))

        # Page canvas and its state
        self._page_widget_grid = QGridLayout()
        self._page_widget_grid.set_contents_margins(0, 0, 0, 0)

        self._current_canvas_widget = QLabel()
        self._current_canvas_widget.set_object_name("CurrentCanvasWidget")
        self._current_canvas_widget.set_text(self.translate("Choose settings category"))
        self._current_canvas_widget.set_alignment(Qt.AlignmentFlag.AlignCenter)

        # Footer layout
        self._command_buttons_footer_grid = QGridLayout()
        self._command_buttons_footer_grid.set_horizontal_spacing(0)
        self._command_buttons_footer_grid.set_contents_margins(0, 0, 0, 0)

        self._footer_button_box = QDialogButtonBox()
        self._footer_button_box.set_contents_margins(0, 10, 10, 10)

        self._ok_button = QPushButton()
        self._ok_button.set_text(self.translate("Ok"))
        self._ok_button.clicked.connect(self._on_pages_accept)

        self._cancel_button = QPushButton()
        self._cancel_button.set_text(self.translate("Cancel"))
        self._cancel_button.clicked.connect(self._on_pages_cancel)

        self._apply_button = QPushButton()
        self._apply_button.set_text(self.translate("Apply"))
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
        self._tree_widget.set_object_name("SettingsTreeWidget")

        self._root_grid = QGridLayout(self._dialog)
        self._root_grid.add_widget(self._tree_widget, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self._root_grid.add_layout(self._page_widget_grid, 0, 1, Qt.AlignmentFlag.AlignHCenter)
        self._root_grid.add_widget(Spacer(), 1, 0, Qt.AlignmentFlag.AlignBottom)
        self._root_grid.add_layout(self._command_buttons_footer_grid, 2, 0, 10, 0)

        self._dialog.set_layout(self._root_grid)
        self._prepare_pages()

    def call(self) -> None:
        self._dialog.show()

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg", section=self.name)

    @on_plugin_event(target=Plugin.MenuBar)
    def on_menu_bar_available(self) -> None:
        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name="settings",
            text=self.translate("Settings"),
            triggered=self.call,
            icon=self.get_svg_icon("icons/settings.svg"),
            before=MainMenuItem.Exit
        )

    def _enable_apply_button(self, state: bool) -> None:
        self._apply_button.set_enabled(state)

    def _prepare_pages(self) -> None:
        pages_dict = self.get_confpages_dict()
        for page in pages_dict.values():
            root_page: ConfigPage = page["page"]
            root_page.init()
            root_page.sig_enable_apply_button.connect(
                lambda: self._enable_apply_button(root_page.is_modified)
            )

            root_tree_item = CustomTreeWidgetItem(root_page)
            if root_page.get_icon():
                root_tree_item.set_icon(0, root_page.get_icon())
                root_tree_item.set_text(1, root_page.get_title())

            root_tree_item.set_text(0, root_page.get_title())

            if len(page["children"]) > 0:
                for child_page in page["children"]:
                    child_page.init()
                    child_tree_item = CustomTreeWidgetItem(child_page)
                    child_tree_item.set_text(0, child_page.get_title())
                    root_tree_item.add_child(child_tree_item)

            self._tree_widget.itemClicked.connect(self._on_item_clicked)
            self._tree_widget.add_top_level_item(root_tree_item)

    @Slot(CustomTreeWidgetItem, int)
    def _on_item_clicked(self, page: CustomTreeWidgetItem) -> None:
        """
        Handle on item clicked event by swapping current widget with the new one

        Args:
            page (CustomTreeWidgetItem): configuration page instance
        """
        # This is a retarded way to swap components but that will do
        self._page_widget_grid.remove_widget(self._current_canvas_widget)
        self._current_canvas_widget.set_visible(False)
        self._current_canvas_widget = page.confpage.get_page_widget()
        self._page_widget_grid.add_widget(self._current_canvas_widget, 0, 0)
        self._current_canvas_widget.set_visible(True)

    def _on_pages_accept(self) -> None:
        pages = self.get_confpages_list()
        for page in pages:
            page.accept()

        self._dialog.accept()

    def _on_pages_cancel(self) -> None:
        # TODO: Add changes tracker subscription
        pages = self.get_confpages_list()
        for page in pages:
            page.cancel()

        self._dialog.accept()

    def _on_pages_apply(self) -> None:
        pages = self.get_confpages_list()
        for page in pages:
            page.accept()


def main(parent: "QMainWindow", plugin_path: "Path"):
    return Settings(parent, plugin_path)

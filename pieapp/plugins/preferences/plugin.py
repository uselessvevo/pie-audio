from typing import Type

from PySide6.QtGui import Qt
from PySide6.QtCore import Slot

from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTreeWidget
from PySide6.QtWidgets import QDialogButtonBox

from pieapp.api.exceptions import PieException
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.registry import Registry
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.menus import MainMenu
from pieapp.api.models.menus import MainMenuItem

from pieapp.api.gloader import Global
from pieapp.api.plugins.confpage import ConfigPage
from pieapp.api.plugins.mixins import CoreAccessorsMixin
from pieapp.api.plugins.mixins import LayoutAccessorsMixins

from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.registries.models import Scope, SysRegistry
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.utils.logger import logger

from pieapp.widgets.spacer import Spacer
from pieapp.widgets.buttons import Button
from pieapp.widgets.buttons import ButtonRole

from preferences.widgets.item import ConfigPageTreeWidgetItem


class Preferences(PiePlugin, CoreAccessorsMixin, LayoutAccessorsMixins):
    name = SysPlugin.Preferences
    requires = [SysPlugin.MainMenuBar]

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg", scope=self.name)

    def init(self) -> None:
        # Define registry
        self._tree_item_index: int = 0
        self._tree_items: dict[str, ConfigPageTreeWidgetItem] = {}
        self._registry: BaseRegistry = Registry(SysRegistry.ConfigPages)

        # Main window dialog
        self._dialog = QDialog(self._parent)
        self._dialog.set_modal(True)
        self._dialog.set_object_name("PreferencesDialog")
        self._dialog.set_window_title(translate("Preferences"))
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.set_minimum_size(*Global.DEFAULT_MIN_WINDOW_SIZE)
        self._dialog.resize(*self.get_config("ui.window_size", Scope.User, Global.DEFAULT_MIN_WINDOW_SIZE))

        # Page canvas and its state
        self._page_widget_grid = QGridLayout()
        self._page_widget_grid.set_spacing(0)
        self._page_widget_grid.set_contents_margins(0, 0, 0, 0)
        self._page_widget_grid.set_alignment(Qt.AlignmentFlag.AlignHCenter)

        self._current_config_page = None
        self._current_widget = QLabel()
        self._current_widget.set_object_name("PreferencesCurrentWidget")
        self._current_widget.set_alignment(Qt.AlignmentFlag.AlignCenter)

        # Footer layout
        self._command_buttons_footer_grid = QGridLayout()
        self._command_buttons_footer_grid.set_horizontal_spacing(0)
        self._command_buttons_footer_grid.set_contents_margins(0, 0, 0, 0)

        self._footer_button_box = QDialogButtonBox()
        self._footer_button_box.set_object_name("PreferencesButtonBox")
        self._footer_button_box.set_contents_margins(0, 10, 10, 10)

        self._ok_button = Button(ButtonRole.Primary)
        self._ok_button.set_text(translate("Ok"))
        self._ok_button.clicked.connect(self._on_pages_accept)

        self._cancel_button = Button()
        self._cancel_button.set_text(translate("Cancel"))
        self._cancel_button.clicked.connect(self._on_pages_cancel)

        self._apply_button = Button()
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

        self._page_widget_grid.add_widget(self._current_widget, 0, 0)

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

    def register_config_page(self, plugin: PiePlugin) -> None:
        plugin_config_page = getattr(plugin, "get_config_page")
        if plugin_config_page and callable(plugin_config_page):
            config_page: ConfigPage = plugin_config_page()
            self._registry.add(plugin.name, config_page)

            config_page.sig_toggle_apply_button.connect(
                lambda: self._toggle_apply_button(config_page._is_modified)
            )
            config_page.sig_toggle_config_page_state.connect(
                lambda: config_page.set_page_state(config_page._is_blocked)
                # lambda: self._toggle_current_page_state(config_page._is_blocked)
            )
            config_page.init()

            tree_item = ConfigPageTreeWidgetItem(config_page, self._tree_item_index)
            if config_page.get_icon():
                tree_item.set_icon(0, config_page.get_icon())
                tree_item.set_text(1, config_page.get_title())

            tree_item.set_text(0, config_page.get_title())
            self._tree_items[plugin.name] = tree_item
            self._tree_widget.add_top_level_item(tree_item)
            self._tree_item_index += 1

    def update_config_page(self, plugin: PiePlugin, new_page_name: str, new_page_class: Type[ConfigPage]) -> None:
        # Update config page widget
        new_page = new_page_class()
        new_page.init()
        new_page.sig_toggle_apply_button.connect(
            lambda: self._toggle_apply_button(new_page.is_modified)
        )

        # Update config page tree item widget
        cur_tree_item = self._tree_items[plugin.name]
        new_tree_item = ConfigPageTreeWidgetItem(new_page, cur_tree_item.index)
        if new_page.get_icon():
            new_tree_item.set_icon(0, new_page.get_icon())
            new_tree_item.set_text(1, new_page.get_title())

        new_tree_item.set_text(0, new_page.get_title())
        del self._tree_items[plugin.name]
        self._tree_items[new_page_name] = new_tree_item
        self._tree_widget.take_top_level_item(cur_tree_item.index)
        self._tree_widget.add_top_level_item(new_tree_item)

    def deregister_config_page(self, plugin: PiePlugin) -> None:
        if plugin.name in self._registry:
            self._registry.remove(plugin.name)
            for index, tree_item in enumerate(self._registry.items()):
                if tree_item.confpage.name == plugin.name:
                    self._tree_widget.remove_item_widget(tree_item, index)

    def _toggle_current_page_state(self, disabled: bool) -> None:
        self._current_config_page.set_disabled(disabled)

    def _toggle_apply_button(self, disable: bool) -> None:
        self._apply_button.set_enabled(disable)

    @Slot(ConfigPageTreeWidgetItem, int)
    def _on_item_clicked(self, page: ConfigPageTreeWidgetItem) -> None:
        """
        Handle on item clicked event by swapping current widget with the new one

        Args:
            page (ConfigPageTreeWidgetItem): configuration page instance
        """
        # This is a retarded way to swap components but that will do
        self._page_widget_grid.remove_widget(self._current_widget)
        self._current_widget.set_visible(False)

        self._current_config_page = page
        self._current_widget = page.confpage.get_page_widget()
        self._current_widget.set_size_policy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._page_widget_grid.add_widget(self._current_widget, 0, 0)
        self._current_widget.set_visible(True)

    def _on_pages_accept(self) -> None:
        pages = self._registry.values()
        for page in pages:
            try:
                page.accept()
            except PieException as e:
                logger.debug(str(e))

        self._dialog.accept()

    def _on_pages_cancel(self) -> None:
        # TODO: Add changes tracker subscription
        pages = self._registry.values()
        for page in pages:
            try:
                page.cancel()
            except PieException as e:
                logger.debug(str(e))

        self._dialog.accept()

    def _on_pages_apply(self) -> None:
        pages = self._registry.values()
        for page in pages:
            try:
                page.accept()
            except PieException as e:
                logger.debug(str(e))

    @on_plugin_available(plugin=SysPlugin.MainMenuBar)
    def _on_menu_bar_available(self) -> None:
        self.add_menu_item(
            scope=Scope.Shared,
            menu=MainMenu.File,
            name="preferences",
            text=translate("Preferences"),
            triggered=self.call,
            icon=self.get_plugin_icon(),
            after=MainMenuItem.OpenFiles
        )


def main(parent: "QMainWindow", plugin_path: "Path"):
    return Preferences(parent, plugin_path)

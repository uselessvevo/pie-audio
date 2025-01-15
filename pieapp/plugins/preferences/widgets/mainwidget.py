from __feature__ import snake_case

from typing import Type

from PySide6.QtGui import Qt
from PySide6.QtCore import Slot, Signal

from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTreeWidget
from PySide6.QtWidgets import QDialogButtonBox

from pieapp.api.globals import Global
from pieapp.api.models.scopes import Scope
from pieapp.api.plugins import ConfigPage
from pieapp.api.plugins.widgets import PiePluginWidget, DialogType
from pieapp.api.registries.confpages.registry import ConfigPageRegistry
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin

from pieapp.widgets.spacer import Spacer
from pieapp.widgets.buttons import Button
from pieapp.widgets.buttons import ButtonRole
from preferences.widgets.item import ConfigPageTreeWidgetItem


class PreferencesWidget(PiePluginWidget, ConfigAccessorMixin):
    dialog_type = DialogType.Dialog
    sig_accept = Signal()
    sig_cancel = Signal()
    sig_apply = Signal()

    def init(self) -> None:
        self._tree_item_index: int = 0
        self._tree_items: dict[str, ConfigPageTreeWidgetItem] = {}

        # Main window dialog
        self.set_object_name("PreferencesDialog")
        self.set_minimum_size(*Global.DEFAULT_WINDOW_SIZE)
        self.resize(*self.get_app_config("config.ui.window_size", Scope.User, Global.DEFAULT_WINDOW_SIZE))

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
        self._ok_button.clicked.connect(self.sig_accept)

        self._cancel_button = Button()
        self._cancel_button.set_text(translate("Cancel"))
        self._cancel_button.clicked.connect(self.sig_cancel)

        self._apply_button = Button()
        self._apply_button.set_text(translate("Apply"))
        self._apply_button.set_enabled(False)
        self._apply_button.clicked.connect(self.sig_apply)

        self._footer_button_box.add_button(self._ok_button, QDialogButtonBox.ButtonRole.AcceptRole)
        self._footer_button_box.add_button(self._cancel_button, QDialogButtonBox.ButtonRole.RejectRole)
        self._footer_button_box.add_button(self._apply_button, QDialogButtonBox.ButtonRole.ApplyRole)

        self._command_buttons_footer_grid.add_widget(Spacer(), 0, 0, Qt.AlignmentFlag.AlignRight)
        self._command_buttons_footer_grid.add_widget(self._footer_button_box, 0, 1, Qt.AlignmentFlag.AlignRight)
        self._page_widget_grid.add_widget(self._current_widget, 0, 0)

        # Tree widget
        self._tree_widget = QTreeWidget()
        self._tree_widget.set_header_hidden(True)
        self._tree_widget.set_indentation(0)
        self._tree_widget.set_object_name("PreferencesTreeWidget")
        self._tree_widget.itemClicked.connect(self._on_item_clicked)

        self._root_grid = QGridLayout(self)
        self._root_grid.add_widget(self._tree_widget, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self._root_grid.add_layout(self._page_widget_grid, 0, 1, Qt.AlignmentFlag.AlignTop)
        self._root_grid.add_widget(Spacer(), 1, 0, Qt.AlignmentFlag.AlignBottom)
        self._root_grid.add_layout(self._command_buttons_footer_grid, 2, 0, 10, 0)

        self.set_layout(self._root_grid)

    def call(self) -> None:
        self.show()

    def register_config_page(self, config_page: ConfigPage) -> None:
        config_page.sig_toggle_apply_button.connect(
            lambda: self._toggle_apply_button(config_page.is_modified)
        )
        config_page.sig_toggle_config_page_state.connect(
            lambda: config_page.set_page_state(config_page.is_blocked)
            # lambda: self._toggle_current_page_state(config_page.is_blocked)
        )
        config_page.init()

        tree_item = ConfigPageTreeWidgetItem(config_page, self._tree_item_index)
        if config_page.get_icon():
            tree_item.set_icon(0, config_page.get_icon())
            tree_item.set_text(1, config_page.get_title())

        tree_item.set_text(0, config_page.get_title())
        self._tree_items[config_page.name] = tree_item
        self._tree_widget.add_top_level_item(tree_item)
        self._tree_item_index += 1

    def register_config_pages(self, config_pages: list[ConfigPage]) -> None:
        for config_page in config_pages:
            config_page.sig_toggle_apply_button.connect(
                lambda: self._toggle_apply_button(config_page.is_modified)
            )
            config_page.sig_toggle_config_page_state.connect(
                lambda: config_page.set_page_state(config_page.is_blocked)
                # lambda: self._toggle_current_page_state(config_page.is_blocked)
            )
            config_page.init()

            tree_item = ConfigPageTreeWidgetItem(config_page, self._tree_item_index)
            if config_page.get_icon():
                tree_item.set_icon(0, config_page.get_icon())
                tree_item.set_text(1, config_page.get_title())

            tree_item.set_text(0, config_page.get_title())
            self._tree_items[config_page.name] = tree_item
            self._tree_widget.add_top_level_item(tree_item)
            self._tree_item_index += 1

    def update_config_page(self, new_page_name: str, new_config_page: ConfigPage) -> None:
        # Update config page widget
        new_config_page.init()
        new_config_page.sig_toggle_apply_button.connect(
            lambda: self._toggle_apply_button(new_config_page.is_modified)
        )

        # Update config page tree item widget
        cur_tree_item = self._tree_items[new_page_name]
        new_tree_item = ConfigPageTreeWidgetItem(new_config_page, cur_tree_item.index)
        if new_config_page.get_icon():
            new_tree_item.set_icon(0, new_config_page.get_icon())
            new_tree_item.set_text(1, new_config_page.get_title())

        new_tree_item.set_text(0, new_config_page.get_title())
        del self._tree_items[new_page_name]
        self._tree_items[new_page_name] = new_tree_item
        self._tree_widget.take_top_level_item(cur_tree_item.index)
        self._tree_widget.add_top_level_item(new_tree_item)

    def deregister_config_page(self, config_page: Type[ConfigPage]) -> None:
        if config_page.name in ConfigPageRegistry:
            ConfigPageRegistry.remove(config_page.name)
            for index, tree_item in enumerate(ConfigPageRegistry.items()):
                if tree_item.confpage.name == config_page.name:
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

from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QSizePolicy, QLineEdit

from pieapp.api.managers.themes.mixins import ThemeAccessorMixin


class ConverterSearch(QLineEdit, ThemeAccessorMixin):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.set_object_name("ConverterSearch")
        self.set_placeholder_text("Search...")
        self.set_attribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.add_action(self.get_svg_icon("icons/search.svg"), QLineEdit.ActionPosition.LeadingPosition)

        self.set_clear_button_enabled(True)
        # self.set_contents_margins(0, 0, 0, 0)
        self.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

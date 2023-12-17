"""
    Elypson/qt-collapsible-section
    (c) 2016 Michael A. Voelkel - michael.alexander.voelkel@gmail.com

    This file is part of Elypson/qt-collapsible section.

    Elypson/qt-collapsible-section is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, version 3 of the License, or
    (at your option) any later version.

    Elypson/qt-collapsible-section is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Elypson/qt-collapsible-section. If not, see <http:#www.gnu.org/licenses/>.
"""
from __feature__ import snake_case

import PySide6.QtCore as cr
import PySide6.QtWidgets as wd


class Collapsable(wd.QWidget):
    def __init__(self, title: str = "", animation_duration: int = 0, parent: cr.QObject = None):
        super().__init__(parent)

        self.animation_duration = animation_duration
        self.toggle_button = wd.QToolButton(self)
        self.header_line = wd.QFrame(self)
        self.toggle_animation = cr.QParallelAnimationGroup(self)
        self.content_area = wd.QScrollArea(self)
        self.main_layout = wd.QGridLayout(self)

        self.toggle_button.set_style_sheet("QToolButton {border: none;}")
        self.toggle_button.set_tool_button_style(cr.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.set_arrow_type(cr.Qt.ArrowType.RightArrow)
        self.toggle_button.set_text(title)
        self.toggle_button.set_checkable(True)
        self.toggle_button.set_checked(False)

        self.header_line.set_frame_shape(wd.QFrame.Shape.NoFrame)
        self.header_line.set_frame_shadow(wd.QFrame.Shadow.Plain)
        self.header_line.set_size_policy(wd.QSizePolicy.Policy.Expanding, wd.QSizePolicy.Policy.Maximum)

        # self.contentArea.setLayout(wd.QHBoxLayout())
        self.content_area.set_size_policy(wd.QSizePolicy.Policy.Expanding, wd.QSizePolicy.Policy.Fixed)

        # start out collapsed
        self.content_area.set_maximum_height(0)
        self.content_area.set_minimum_height(0)

        # let the entire widget grow and shrink with its content
        self.toggle_animation.add_animation(cr.QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.add_animation(cr.QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.add_animation(cr.QPropertyAnimation(self.content_area, b"maximumHeight"))

        self.main_layout.set_vertical_spacing(0)
        self.main_layout.set_contents_margins(0, 0, 0, 0)

        row = 0
        self.main_layout.add_widget(self.toggle_button, row, 0, 1, 1, cr.Qt.AlignmentFlag.AlignLeft)
        self.main_layout.add_widget(self.header_line, row, 2, 1, 1)
        self.main_layout.add_widget(self.content_area, row + 1, 0, 1, 3)
        self.set_layout(self.main_layout)

        self.toggle_button.toggled.connect(self.toggle)

    def set_content_layout(self, content_layout):
        self.content_area.set_layout(content_layout)
        collapsed_height = self.size_hint().height() - self.content_area.maximum_height()
        content_height = content_layout.size_hint().height()

        for ta in range(0, self.toggle_animation.animation_count() - 1):
            section_animation = self.toggle_animation.animation_at(ta)
            section_animation.set_duration(self.animation_duration)
            section_animation.set_start_value(collapsed_height)
            section_animation.set_end_value(collapsed_height + content_height)

        content_animation = self.toggle_animation.animation_at(self.toggle_animation.animation_count() - 1)
        content_animation.set_duration(self.animation_duration)
        content_animation.set_start_value(0)
        content_animation.set_end_value(content_height)

    def toggle(self, collapsed):
        if collapsed:
            self.toggle_button.set_arrow_type(cr.Qt.ArrowType.DownArrow)
            self.toggle_animation.set_direction(cr.QAbstractAnimation.Direction.Forward)
        else:
            self.toggle_button.set_arrow_type(cr.Qt.ArrowType.RightArrow)
            self.toggle_animation.set_direction(cr.QAbstractAnimation.Direction.Backward)
        self.toggle_animation.start()

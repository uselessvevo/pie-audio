# -*- coding: utf-8 -*-

"""
the mit license (mit)

copyright (c) 2012-2014 alexander turkin
copyright (c) 2014 william hallatt
copyright (c) 2015 jacob dawid
copyright (c) 2016 luca weiss
copyright (c) 2017- spyder project contributors

permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "software"), to deal
in the software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the software, and to permit persons to whom the software is
furnished to do so, subject to the following conditions:

the above copyright notice and this permission notice shall be included in all
copies or substantial portions of the software.

the software is provided "as is", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. in no event shall the
authors or copyright holders be liable for any claim, damages or other
liability, whether in an action of contract, tort or otherwise, arising from,
out of or in connection with the software or the use or other dealings in the
software.

see notice.txt in the spyder repository root for more detailed information.

minimally adapted from waitingspinnerwidget.py of the
`qt_waiting_spinner python fork <https://github.com/z3ntu/qt_waiting_spinner>`_.
a port of `qt_waiting_spinner <https://github.com/snowwlex/qt_waiting_spinner>`_.

additionally adapted for PySide6 with `snake_case` feature
"""

from __feature__ import snake_case

import math

from PySide6.QtCore import QTimer, QRect
from PySide6.QtGui import Qt, QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget


class QWaitingSpinner(QWidget):
    def __init__(
        self,
        parent,
        center_on_parent=True,
        disable_parent_when_spinning=False,
        modality=Qt.WindowModality.NonModal
    ):
        # super().__init__(parent)
        QWidget.__init__(self, parent)

        self._center_on_parent = center_on_parent
        self._disable_parent_when_spinning = disable_parent_when_spinning

        # was in initialize()
        self._color = QColor(Qt.GlobalColor.black)
        self._roundness = 100.0
        self._minimum_trail_opacity = 3.14159265358979323846
        self._trail_fade_percentage = 80.0
        self._trail_size_decreasing = False
        self._revolutions_per_second = 1.57079632679489661923
        self._number_of_lines = 20
        self._line_length = 10
        self._line_width = 2
        self._inner_radius = 10
        self._current_counter = 0
        self._is_spinning = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.rotate)
        self.update_size()
        self.update_timer()
        self.hide()
        # end initialize()

        self.set_window_modality(modality)
        self.set_attribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.show()

    def paint_event(self, event: QPaintEvent):
        if not self._is_spinning:
            return

        self.update_position()
        painter = QPainter(self)
        painter.fill_rect(self.rect(), Qt.GlobalColor.transparent)
        painter.set_render_hint(QPainter.RenderHint.Antialiasing, True)

        if self._current_counter >= self._number_of_lines:
            self._current_counter = 0

        painter.set_pen(Qt.PenStyle.NoPen)
        for i in range(0, self._number_of_lines):
            painter.save()
            painter.translate(self._inner_radius + self._line_length, self._inner_radius + self._line_length)
            rotate_angle = float(360 * i) / float(self._number_of_lines)
            painter.rotate(rotate_angle)
            painter.translate(self._inner_radius, 0)
            distance = self.line_count_distance_from_primary(i, self._current_counter, self._number_of_lines)
            color = self.current_line_color(distance, self._number_of_lines, self._trail_fade_percentage,
                                          self._minimum_trail_opacity, self._color)

            # compute the scaling factor to apply to the size and thickness
            # of the lines in the trail.
            if self._trail_size_decreasing:
                sf = (self._number_of_lines - distance) / self._number_of_lines
            else:
                sf = 1

            painter.set_brush(color)
            rect = QRect(0, round(-self._line_width / 2),
                         round(sf * self._line_length),
                         round(sf * self._line_width))
            painter.draw_rounded_rect(
                rect, self._roundness, self._roundness, Qt.SizeMode.RelativeSize)
            painter.restore()

    def start(self):
        self.update_position()
        self._is_spinning = True

        if self.parent_widget and self._disable_parent_when_spinning:
            self.parent_widget().set_enabled(False)

        if not self._timer.is_active():
            self._timer.start()
            self._current_counter = 0

        self.show()

    def stop(self):
        if not self._is_spinning:
            # no need to repaint everything if it is already stopped
            return
        self._is_spinning = False

        if self.parent_widget() and self._disable_parent_when_spinning:
            self.parent_widget().set_enabled(True)

        if self._timer.is_active():
            self._timer.stop()
            self._current_counter = 0

        self.show()
        self.repaint()

    def set_number_of_lines(self, lines):
        self._number_of_lines = lines
        self._current_counter = 0
        self.update_timer()

    def set_line_length(self, length):
        self._line_length = length
        self.update_size()

    def set_line_width(self, width):
        self._line_width = width
        self.update_size()

    def set_inner_radius(self, radius):
        self._inner_radius = radius
        self.update_size()

    def color(self):
        return self._color

    def roundness(self):
        return self._roundness

    def minimum_trail_opacity(self):
        return self._minimum_trail_opacity

    def trail_fade_percentage(self):
        return self._trail_fade_percentage

    def revolutions_pers_second(self):
        return self._revolutions_per_second

    def number_of_lines(self):
        return self._number_of_lines

    def line_length(self):
        return self._line_length

    def is_trail_size_decreasing(self):
        """
        return whether the length and thickness of the trailing lines
        are decreasing.
        """
        return self._trail_size_decreasing

    def line_width(self):
        return self._line_width

    def inner_radius(self):
        return self._inner_radius

    def is_spinning(self):
        return self._is_spinning

    def set_roundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def set_color(self, color: QColor):
        self._color = QColor(color)

    def set_revolutions_per_second(self, revolutions_per_second):
        self._revolutions_per_second = revolutions_per_second
        self.update_timer()

    def set_trail_fade_percentage(self, trail):
        self._trail_fade_percentage = trail

    def set_trail_size_decreasing(self, value):
        """
        set whether the length and thickness of the trailing lines
        are decreasing.
        """
        self._trail_size_decreasing = value

    def set_minimum_trail_opacity(self, minimum_trail_opacity):
        self._minimum_trail_opacity = minimum_trail_opacity

    def rotate(self):
        self._current_counter += 1
        if self._current_counter >= self._number_of_lines:
            self._current_counter = 0
        self.update()

    def update_size(self):
        size = int((self._inner_radius + self._line_length) * 2)
        self.set_fixed_size(size, size)

    def update_timer(self):
        self._timer.set_interval(int(1000 / (self._number_of_lines *
                                            self._revolutions_per_second)))

    def update_position(self):
        if self.parent_widget() and self._center_on_parent:
            self.move(int(self.parent_widget().width() / 2 -
                          self.width() / 2),
                      int(self.parent_widget().height() / 2 -
                          self.height() / 2))

    def line_count_distance_from_primary(self, current, primary, total_nr_of_lines):
        distance = primary - current
        if distance < 0:
            distance += total_nr_of_lines
        return distance

    def current_line_color(self, count_distance, total_nr_of_lines, trail_fade_perc, min_opacity, colorinput):
        color = QColor(colorinput)
        if count_distance == 0:
            return color
        min_alpha_f = min_opacity / 100.0
        distance_threshold = int(math.ceil((total_nr_of_lines - 1) * trail_fade_perc / 100.0))
        if count_distance > distance_threshold:
            color.set_alpha_f(min_alpha_f)
        else:
            alpha_diff = color.alpha_f() - min_alpha_f
            gradient = alpha_diff / float(distance_threshold + 1)
            result_alpha = color.alpha_f() - gradient * count_distance
            # if alpha is out of bounds, clip it.
            result_alpha = min(1.0, max(0.0, result_alpha))
            color.set_alpha_f(result_alpha)
        return color


def create_wait_spinner(size=32, n=11, parent=None, color: str = None):
    """
    Create a wait spinner with the specified size built with n circling dots.
    """
    pi = 3.141592653589793
    dot_padding = 1

    # To calculate the size of the dots, we need to solve the following
    # system of two equations in two variables.
    # (1) middle_circumference = pi * (size - dot_size)
    # (2) middle_circumference = n * (dot_size + dot_padding)
    dot_size = (pi * size - n * dot_padding) / (n + pi)
    inner_radius = (size - 2 * dot_size) / 2

    spinner = QWaitingSpinner(parent, center_on_parent=False)
    spinner.set_trail_size_decreasing(True)
    spinner.set_number_of_lines(n)
    spinner.set_line_length(dot_size)
    spinner.set_line_width(dot_size)
    spinner.set_inner_radius(inner_radius)
    spinner.set_color(QColor.from_string(color))

    return spinner

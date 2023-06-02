from __feature__ import snake_case
from PySide6.QtCore import QRect, QPoint
from PySide6.QtWidgets import QTabWidget, QTabBar, QStylePainter, QStyleOptionTab, QStyle


class TabBar(QTabBar):

    def tab_size_hint(self, index):
        size_hint = QTabBar.tab_size_hint(self, index)
        size_hint.transpose()
        return size_hint

    def paint_event(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionTab()

        for i in range(self.count()):
            self.init_style_option(option, i)
            painter.draw_control(QStyle.ControlElement.CE_TabBarTabShape, option)
            painter.save()

            rect_size = option.rect.size()
            rect_size.transpose()
            rect = QRect(QPoint(), rect_size)
            rect.move_center(option.rect.center())
            option.rect = rect

            tab_rect_center = self.tab_rect(i).center()
            painter.translate(tab_rect_center)
            painter.rotate(90)
            painter.translate(-tab_rect_center)
            painter.draw_control(QStyle.ControlElement.CE_TabBarTabLabel, option)
            painter.restore()


class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)
        self.set_tab_bar(TabBar(self))
        self.set_tab_position(QTabWidget.TabPosition.West)

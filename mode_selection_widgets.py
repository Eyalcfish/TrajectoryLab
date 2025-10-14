
from custom_widgets import EventMixin, State, fit_text_to_widget
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QPushButton, QSizePolicy, QWidget
from PySide6.QtGui import QColor

class blankWidget(EventMixin, QWidget): 
    def __init__(self, x, y, w, h, debug=False, parent=None):
        super().__init__(parent)
        self.x_pos = x
        self.y_pos = y
        self.w = w
        self.h = h

        parent_w = self.parent().width()
        parent_h = self.parent().height()
        self.setGeometry(self.x_pos * parent_w, self.y_pos * parent_h, self.w * parent_w, self.h * parent_h)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.debug(debug)

    def debug(self, mode):
        if mode:
            print("Debug mode is ON")
            self.setStyleSheet("background-color: red;")
            self.raise_()
        else:
            self.setStyleSheet("background-color: transparent;")
            self.lower()
        self.cupdate(State.DEFAULT)


    def cupdate(self, state: State):
        parent_w = self.parent().width()
        parent_h = self.parent().height()
        if state == State.RESIZE:
            for child in self.findChildren(QWidget):
                if hasattr(child, "cupdate"):
                    child.cupdate(State.RESIZE)
        self.setGeometry(self.x_pos * parent_w, self.y_pos * parent_h, self.w * parent_w, self.h * parent_h)


class PopUpButton(EventMixin, QPushButton):
    def __init__(self, text, w, h, pop_offset=0.2, popped=False, background_color="#3498db", parent=None):
        super().__init__(text, parent)
        self.pop_offset = pop_offset
        self.background_color = background_color
        self.base_pos = None
        self.w = w
        self.h = h
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        self.m = min(self.w*self.parent_w, self.h*self.parent_h)

        self.hover_anim = QPropertyAnimation(self, b"pos")
        self.hover_anim.setDuration(150)
        self.hover_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.popped = popped

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet(self._stylesheet(self.background_color))
        self.parent_w = self.parent().width()
        fit_text_to_widget(self, text=self.text(), padding=self.m*0.2)

    def cupdate(self, state: State):
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        self.m = min(self.w*self.parent_w, self.h*self.parent_h)
        self.resize(self.parent_w * self.w, self.parent_h * self.h)

        if self.base_pos is None or state == State.DEFAULT:
            self.base_pos = self.pos()

        if state == State.REPAINT or state == State.RESIZE:
            if self.popped:
                self.move(self.base_pos + self._offset_vector())
            else:
                self.hover_anim.stop()
                self.hover_anim.setStartValue(self.pos())
                self.hover_anim.setEndValue(self.base_pos)
                self.hover_anim.start()
            self.setStyleSheet(self._stylesheet(self.background_color))
            QTimer.singleShot(0, lambda: fit_text_to_widget(self, text=self.text(), padding=self.m*0.1))

        if state == State.ENTER_HOVER and not self.popped:
            self.hover_anim.stop()
            self.hover_anim.setStartValue(self.pos())
            self.hover_anim.setEndValue(self.base_pos + self._offset_vector())
            self.hover_anim.start()

        elif state == State.LEAVE_HOVER and not self.popped:
            self.hover_anim.stop()
            self.hover_anim.setStartValue(self.pos())
            self.hover_anim.setEndValue(self.base_pos)
            self.hover_anim.start()

    def pop_up(self, condition):
        self.popped = condition
        self.cupdate(State.REPAINT)


    def _stylesheet(self, color):
        if self.popped:
            hover_color = QColor("#22C55E").lighter(150).name()
            return f"""
                QPushButton {{
                    background-color: #22C55E;
                    border: none;
                    color: black;
                    border-radius: {self.m*0.12}px;
                    padding: {self.m*0.1}px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                }}
                QPushButton:pressed {{
                    background-color: #22C55E;
                }}
            """
        else:
            hover_color = QColor(color).lighter(120).name()
            return f"""
                QPushButton {{
                    background-color: {color};
                    border: none;
                    color: white;
                    border-radius: {self.m*0.12}px;
                    padding: {self.m*0.1}px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                }}
                QPushButton:pressed {{
                    background-color: {color};
                }}
            """

    def _offset_vector(self):
        return QPoint(self.pop_offset*self.parent_w, 0)
        
from custom_widgets import EventMixin, State, fit_text_to_widget
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QPushButton, QSizePolicy, QWidget, QLineEdit, QLabel
from PySide6.QtGui import QDoubleValidator, Qt

class ResultShowcaseWidget(EventMixin, QWidget):
    CONTAINER = 0
    LINE = 1
    def __init__(self, x, y, w, h, result, removal_function, parent = None, background_color = "#FFFFFF"):
        super().__init__(parent)
        self.x_pos = x
        self.y_pos = y
        self.w = w
        self.h = h
        self.background_color = background_color
        self.result = result
        self.removal_function = removal_function
        self.line = QWidget(self)

        self.cupdate(State.DEFAULT)

    def cupdate(self, state: State):    
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        self.m = min(self.w*self.parent_w, self.h*self.parent_h)
        if state == State.DEFAULT:
            self.setAttribute(Qt.WA_StyledBackground, True)
            
        if state == State.RESIZE or state == State.DEFAULT:

            self.setFixedSize(0.8 * self.parent_w, 0.8 * self.parent_h)
            self.move(0.2 * self.parent_w, 0.1 * self.parent_h)
            self.line.setGeometry(0.1*self.w*self.parent_w, 0.9 * self.h * self.parent_h, 0.8 * self.parent_w*self.w, 0.03 * self.h * self.parent_h)
            
            self.setStyleSheet(self._stylesheet())

    def _stylesheet(self, state=None):
        if state == self.CONTAINER or state is None:
            return f"""
            background-color: {self.background_color};
            border-radius: 12px;
            """
        if state == self.LINE:
            return f"""
            background-color: #FF0000;
            border-radius: {self.m*0.01}px;
            """

from TrajectoryLab.custom_widgets import EventMixin, State, fit_text_to_widget
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

class sideBarButton(EventMixin, QPushButton):
    def __init__(self, text, pressed, x, h, parent=None):
        super().__init__(text, parent)
        self.h = h
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        self.mode = text
        self.w = self.parent_w
        self.x_pos = x
        self.pressed = pressed
        self.y_pos = 0
        self.m = min(self.parent_w, self.h*self.parent_h)
        self.cupdate(state=State.DEFAULT)

    def cupdate(self, state: State):
        if state == State.REPAINT or state == State.RESIZE or state == State.DEFAULT:
            self.setStyleSheet(self._stylesheet(pressed=self.pressed))
            self.parent_w = self.parent().width()
            self.parent_h = self.parent().height()
            self.m = min(self.w, self.parent_h*self.h)
            self.setFixedSize(self.parent_w*0.9, self.parent_h*self.h)
            fit_text_to_widget(self, text=str(self.mode), padding=0)
            self.move(self.x_pos * self.parent_w, self.y_pos * self.parent_h)

    def _stylesheet(self, pressed):
        if pressed:
            return f"""
                QPushButton {{
                    background-color: #38BDF8;
                    border: {self.m*0.05}px solid #1E40AF;
                    color: #E6F0FF;
                    border-radius: {self.m*0.1}px;
                    padding: {self.m*0.05}px;
                }}
                QPushButton:hover {{
                    background-color: #38BDF8;
                }}
                QPushButton:pressed {{
                    background-color: #38BDF8;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: #3B82F6;
                    border: none;
                    color: #E6F0FF;
                    border-radius: {self.m*0.1}px;
                    padding: {self.m*0.05}px;
                }}
                QPushButton:hover {{
                    background-color: #38BDF8;
                }}
                QPushButton:pressed {{
                    background-color: #3B82F6;
                }}
            """
    
class sideBar(EventMixin, QWidget):
    def __init__(self, text, w, pos, parent = None):
        super().__init__(parent)
        self.text = text
        self.w = w
        self.cpos = pos
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        self.m = min(self.w*self.parent_w, self.parent_h)
        self.buttons: list[(sideBarButton, blankWidget)] = []
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.cupdate(state=State.DEFAULT)
    
    def add_button(self, button: sideBarButton):
        button.setParent(self)
        self.buttons.append(button)
        self.cupdate(State.CHILD_ADDED)

    def cupdate(self, state: State):
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        self.m = min(self.w*self.parent_w, self.parent_h)
        self.setFixedSize(self.w * self.parent_w, self.parent_h)
        if state == State.DEFAULT or state == State.RESIZE:
            if self.cpos == "left":
                self.move(0, 0)
            elif self.cpos == "right":
                self.move(self.parent_w - self.w * self.parent_w, 0)
            self.setStyleSheet(self._stylesheet())
        if state == State.CHILD_ADDED or state == State.RESIZE or state == State.DEFAULT:
            y_offset = 0.01
            for button in self.buttons:
                button.y_pos = y_offset
                y_offset += button.h+0.01
                button.cupdate(State.RESIZE)

    def _stylesheet(self): #1A1A1A
        return f"""
            background-color: #0D0D0D; 
            border-right: {self.m*0.01}px solid #1F1F1F;
            border-radius: 0px;
        """

# class PopUpButton(EventMixin, QPushButton):
#     def __init__(self, text, w, h, pop_offset=0.2, popped=False, background_color="#FFA94D", selected_color="#FF7A00", parent=None):
#         super().__init__(text, parent)
#         self.pop_offset = pop_offset
#         self.background_color = background_color
#         self.selcted_color = selected_color
#         self.base_pos = None
#         self.w = w
#         self.h = h
#         self.parent_w = self.parent().width()
#         self.parent_h = self.parent().height()
#         self.m = min(self.w*self.parent_w, self.h*self.parent_h)

#         self.hover_anim = QPropertyAnimation(self, b"pos")
#         self.hover_anim.setDuration(150)
#         self.hover_anim.setEasingCurve(QEasingCurve.OutQuad)
#         self.popped = popped

#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#         self.parent_w = self.parent().width()
#         self.cupdate(state=State.DEFAULT)

#     def cupdate(self, state: State):
#         self.parent_w = self.parent().width()
#         self.parent_h = self.parent().height()
#         self.m = min(self.w*self.parent_w, self.h*self.parent_h)
#         self.resize(self.parent_w * self.w, self.parent_h * self.h)

#         if self.base_pos is None or state == State.DEFAULT:
#             self.base_pos = self.pos()

#         if state == State.REPAINT or state == State.RESIZE:
#             if self.popped:
#                 self.move(self.base_pos + self._offset_vector())
#             else:
#                 self.hover_anim.stop()
#                 self.hover_anim.setStartValue(self.pos())
#                 self.hover_anim.setEndValue(self.base_pos)
#                 self.hover_anim.start()
#             self.setStyleSheet(self._stylesheet())
#             QTimer.singleShot(0, lambda: fit_text_to_widget(self, text=self.text(), padding=self.m*0.1))

#         if state == State.ENTER_HOVER and not self.popped:
#             self.hover_anim.stop()
#             self.hover_anim.setStartValue(self.pos())
#             self.hover_anim.setEndValue(self.base_pos + self._offset_vector())
#             self.hover_anim.start()

#         elif state == State.LEAVE_HOVER and not self.popped:
#             self.hover_anim.stop()
#             self.hover_anim.setStartValue(self.pos())
#             self.hover_anim.setEndValue(self.base_pos)
#             self.hover_anim.start()

#     def pop_up(self, condition):
#         self.popped = condition
#         self.cupdate(State.REPAINT)

#     def _stylesheet(self):
#         if self.popped:
#             color = self.selcted_color
#         else:
#             color = self.background_color
#         hover_color = QColor(color).lighter(120).name()
#         return f"""
#             QPushButton {{
#                 background-color: {color};
#                 border: none;
#                 color: white;
#                 border-radius: {self.m*0.12}px;
#                 padding: {self.m*0.1}px;
#             }}
#             QPushButton:hover {{
#                 background-color: {hover_color};
#             }}
#             QPushButton:pressed {{
#                 background-color: {color};
#             }}
#         """

#     def _offset_vector(self):
#         return QPoint(self.pop_offset*self.parent_w, 0)
        
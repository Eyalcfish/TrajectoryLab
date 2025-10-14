from custom_widgets import EventMixin, State, fit_text_to_widget
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QPushButton, QSizePolicy, QWidget, QLineEdit, QLabel

class SettingWidget(EventMixin, QWidget):
    CONTAINER = 0
    LINEEDIT = 1
    LABEL = 2
    def __init__(self, default_value, setting_name = "Setting", parent = None, w = 0.5, h = 0.1, background_color = "#ffffff"):
        super().__init__(parent)
        self.w = w
        self.h = h
        self.background_color = background_color

        self.lineedit = QLineEdit(self)
        self.label = QLabel(setting_name, self)

        self.default_value = default_value
        self.setting_name = setting_name
        
        self.cupdate(State.DEFAULT)
 
    def cupdate(self, state: State):    
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        self.m = min(self.w*self.parent_w, self.h*self.parent_h)
        if state == State.DEFAULT:
            self.setAttribute(Qt.WA_StyledBackground, True)
            self.lineedit.setPlaceholderText(str(self.default_value))
            
        if state == State.RESIZE or state == State.DEFAULT:

            self.setFixedSize(self.w * self.parent_w, self.h * self.parent_h)
            self.setStyleSheet(self._stylesheet(self.CONTAINER))

            fit_text_to_widget(self.lineedit, text=str(self.default_value), padding=0)
            self.lineedit.setGeometry(0.55*self.w*self.parent_w, 0.15*self.h*self.parent_h, 0.41*self.w*self.parent_w, 0.75*self.h*self.parent_h)
            self.lineedit.setStyleSheet(self._stylesheet(self.LINEEDIT))

            fit_text_to_widget(self.label, text=str(self.setting_name), padding=0)
            self.label.setGeometry(0, 0, 0.5*self.w*self.parent_w, self.h*self.parent_h)
            self.label.setStyleSheet(self._stylesheet(self.LABEL))
        
    def _stylesheet(self, widget):
        if widget == self.CONTAINER:
            return f"""
            background-color: {self.background_color};
            border-radius: {self.m*0.12}px;
            """
        elif widget == self.LINEEDIT:
            return f"""
            background-color: #ffffff;
            border: None;
            border-radius: 0px;
            padding: {self.m*0.03}px;
            color: #1E293B
            """
        elif widget == self.LABEL:
            return f"""
            background-color: transparent;
            border: none;
            padding: 0px;
            """
        
class SettingWidgetContainer(EventMixin, QWidget):
    def __init__(self, space = 0.25, category_name = "Category", parent = None, w = 0.5, h = 0.1, x = 0, y = 0, background_color = "#ffffff"):
        super().__init__(parent)
        self.w = w
        self.h = h
        self.x_pos = x
        self.y_pos = y
        self.background_color = background_color
        self.space = space

        self.label = QLabel(category_name, self)

        self.settings = []
        self.category_name = category_name
        
        self.cupdate(State.DEFAULT)

    def add_setting(self, setting: SettingWidget):
        self.settings.append(setting)
        setting.setParent(self)
        self.cupdate(State.CHILD_ADDED)

    def cupdate(self, state: State):
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        self.m = min(self.w*self.parent_w, self.h*self.parent_h)
        if state == State.DEFAULT:
            self.setAttribute(Qt.WA_StyledBackground, True)
            
        if state == State.RESIZE or state == State.DEFAULT or state == State.CHILD_ADDED:

            self.setGeometry(self.x_pos*self.parent_w, self.y_pos*self.parent_h, self.w * self.parent_w, self.h * self.parent_h)
            self.setStyleSheet(self._stylesheet())

            fit_text_to_widget(self.label, text=str(self.category_name), padding=0)
            self.label.setGeometry(0.2*self.w*self.parent_w, 0, 0.6*self.w*self.parent_w, 0.3*self.h*self.parent_h)
            self.label.setStyleSheet(self._stylesheet())

            for i, setting in enumerate(self.settings):
                setting.move(0, (0.35 + i*self.space)*self.h*self.parent_h)
                setting.cupdate(State.RESIZE)

    def _stylesheet(self, widget=None):
        if widget is None:
            return f"""
            background-color: {self.background_color};
            border-radius: {self.m*0.05}px;
            """
        elif widget == self.LABEL:
            return f"""
            background-color: transparent;
            border: none;
            padding: 0px;
            """
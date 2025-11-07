from custom_widgets import EventMixin, State, fit_text_to_widget
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QPushButton, QSizePolicy, QWidget, QLineEdit, QLabel, QFrame, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView, QAbstractScrollArea
from PySide6.QtGui import QDoubleValidator, Qt,QColor
from filemanagment import Result, list_of_results
import csv

class CSVEditWidget(EventMixin, QFrame):
    def __init__(self, x, y, w, h, result: Result, parent = None, background_color = "red"):
        super().__init__(parent)
        self.x_pos = x
        self.y_pos = y
        self.w = w
        self.h = h
        self.background_color = background_color
        self. result = result

        self.csvdisplay = CSVDisplay(x=0.70, y=0, w=0.3, h=1, parent=self, background_color={self.background_color})
        if result.csv_path != "":
            self.csvdisplay.load_csv(result.csv_path)

        self.cupdate(State.DEFAULT)

    def cupdate(self, state: State):    
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        self.m = min(self.w*self.parent_w, self.h*self.parent_h)
        if state == State.DEFAULT:
            self.setAttribute(Qt.WA_StyledBackground, True)
            self.csvdisplay.setAttribute(Qt.WA_StyledBackground, True)
            
        if state == State.RESIZE or state == State.DEFAULT:

            self.setGeometry(self.x_pos * self.parent_w, self.y_pos * self.parent_h, self.w * self.parent_w, self.h * self.parent_h)
            self.csvdisplay.cupdate(State.RESIZE)
            
            self.setStyleSheet(self._stylesheet())
            self.raise_()
    
    def _stylesheet(self):
        return f"""
            QFrame {{
                background-color: {self.background_color};
                border-radius: {self.m*0.04}px;
            }}
        """
    
class CSVDisplay(EventMixin, QFrame):
    def __init__(self, x, y, w, h, parent=None, background_color="red"):
        super().__init__(parent)
        self.x_pos = x
        self.y_pos = y
        self.w = w
        self.h = h
        self.background_color = background_color

        self.table = QTableWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.cupdate(State.DEFAULT)
        
    def load_csv(self, path: str):
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = list(csv.reader(f))
                if not reader:
                    return

                headers = reader[0]
                rows = reader[1:]

                self.table.setColumnCount(len(headers))
                self.table.setHorizontalHeaderLabels(headers)
                self.table.setRowCount(len(rows))

                for r, row in enumerate(rows):
                    for c, val in enumerate(row):
                        self.table.setItem(r, c, QTableWidgetItem(val))

                header = self.table.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.Stretch)
                header.setMinimumSectionSize(1)

                self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
                self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

                self.table.resizeRowsToContents()
        except Exception as e:
            pass

    def cupdate(self, state: State):
        if not self.parent():
            return
        parent_w = self.parent().width()
        parent_h = self.parent().height()
        self.m = min(self.w * parent_w, self.h * parent_h)

        if state == State.DEFAULT:
            self.setAttribute(Qt.WA_StyledBackground, True)
        if state in (State.RESIZE, State.DEFAULT):
            self.setGeometry(
                self.x_pos * parent_w,
                self.y_pos * parent_h,
                self.w * parent_w,
                self.h * parent_h
            )
            self.setStyleSheet(self._stylesheet())

    def _stylesheet(self):
        return f"""
            QFrame {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0d1117,
                    stop:1 #161b22
                );
            }}

            QTableWidget {{
                background-color: {self.background_color};
                color: white;
                gridline-color: #1A1A1A;
                selection-background-color: #1f6feb;
                selection-color: white;
                border: none;
                font-family: "Inter", "Roboto", sans-serif;
                font-size: 13px;
            }}

            QHeaderView::section {{
                background-color: #1e293b;
                color: #ffffff;
                font-weight: bold;
            }}

            QScrollBar:vertical {{
                background: #0F0F0F;
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #3F3F3F;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #0F0F0F;
            }}
        """


class ResultShowcaseWidget(EventMixin, QPushButton):
    CONTAINER = 0
    LINE = 1
    BUTTON = 2
    LABEL = 3
    def __init__(self, x, y, w, h, result: Result, removal_function, parent = None, background_color = "red"):
        super().__init__(parent)
        self.x_pos = x
        self.y_pos = y
        self.w = w
        self.h = h
        self.background_color = background_color
        self.result = result
        self.removal_function = removal_function
        self.line = QFrame(self)
        self.remove_button = QPushButton("X", self)
        self.label = QLabel("profile "+str(result.id), self)

        self.editwidget = CSVEditWidget(x=0, y=0.05, w=1, h=1, result=result, parent=parent, background_color="#2A2A2A")
        self.editwidget.hide()
        self.cupdate(State.DEFAULT)

    def toggleeditmode(self):
        if self.editwidget.isVisible():
            self.editwidget.hide()
        else:
            self.editwidget.show()
            self.editwidget.raise_()

    def cupdate(self, state: State):    
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        self.m = min(self.w*self.parent_w, self.h*self.parent_h)
        if state == State.DEFAULT:

            self.setAttribute(Qt.WA_StyledBackground, True)
            self.line.setAttribute(Qt.WA_StyledBackground, True)
            self.remove_button.setAttribute(Qt.WA_StyledBackground, True)
            self.label.setAttribute(Qt.WA_StyledBackground, True)
            self.remove_button.raise_()
            self.clicked.connect(self.toggleeditmode)
            self.remove_button.clicked.connect(self.removal_function)
            
        if state == State.RESIZE or state == State.DEFAULT:

            self.setGeometry(self.x_pos * self.parent_w, self.y_pos * self.parent_h, self.w * self.parent_w, self.h * self.parent_h)
            self.line.setGeometry(0.03*self.w*self.parent_w, 0.1 * self.h * self.parent_h, 0.92 * self.parent_w*self.w, 0.03 * self.h * self.parent_h)
            self.remove_button.setGeometry(0.8*self.w*self.parent_w, 0.15*self.h*self.parent_h, min(self.w*self.parent_w, self.h*self.parent_h)*0.15,min(self.w*self.parent_w, self.h*self.parent_h)*0.15)
            self.label.setGeometry(0.05*self.w*self.parent_w, 0, 0.9*self.w*self.parent_w, 0.1*self.h*self.parent_h)
            fit_text_to_widget(self.label, "profile "+str(self.result.id), padding=0)
            fit_text_to_widget(self.remove_button, "X", padding=2)
            
            self.setStyleSheet(self._stylesheet(self.CONTAINER))
            self.line.setStyleSheet(self._stylesheet(self.LINE))
            self.label.setStyleSheet(self._stylesheet(self.LABEL))
            self.remove_button.setStyleSheet(self._stylesheet(self.BUTTON))

    def _stylesheet(self, state=None):
        if state == self.CONTAINER or state is None:
            lighter_color = QColor(self.background_color).lighter(170).name()
            return f"""
                QPushButton {{
                    background-color: {self.background_color};
                    border-radius: {self.m*0.04}px;
                }}
                QPushButton:hover {{
                    background-color: {lighter_color};
                }}
                QPushButton:pressed {{
                    background-color: {self.background_color};
                }}
            """
        if state == self.LABEL:
            return f"""
                background-color: #0D0D0D;
                border-radius: {self.m*0.01}px;
                color: #FFFFFF;
                """
        
        if state == self.LINE:
            return f"""
            background-color: #38BDF8;
            border-radius: {self.m*0.01}px;
            """
        if state == self.BUTTON:
            return f"""
                QPushButton {{
                    background-color: #FE1A1A;
                    border-radius: {self.m*0.02}px;
                    color: #E6F0FF;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #FF7A7A;
                }}
                QPushButton:pressed {{
                    background-color: #FE1A1A;
                }}

            """
        
class CSVGrid(EventMixin, QFrame):
    def __init__(self, x, y, w, h, results, parent=None, background_color="red"):
        super().__init__(parent)
        self.x_pos = x
        self.y_pos = y
        self.w = w
        self.h = h
        self.background_color = background_color
        self.results = []
        self.widgets = []

        self.update_results(results)

        self.cupdate(State.DEFAULT)

    def update_results(self, results: list[Result]):
        self.results = results
        self.turn_results_into_widgets()

    def turn_results_into_widgets(self):
        for widget in self.widgets:
            widget.setParent(None)
            widget.hide()
            widget.deleteLater()
        self.widgets = []
        for result in self.results:
            widget = ResultShowcaseWidget(x=0, y=0, w=0.1, h=0.1, removal_function=lambda: self.remove_result(0),  result=result, parent=self, background_color="#0D0D0D")
            self.widgets.append(widget)
        self.cupdate(State.RESIZE)

    def remove_result(self, id):
        self.results = [res for res in self.results if res.id != id]
        self.turn_results_into_widgets()

    def cupdate(self, state: State):
        if not self.parent():
            return
        parent_w = self.parent().width()
        parent_h = self.parent().height()
        self.m = min(self.w * parent_w, self.h * parent_h)

        if state == State.DEFAULT:
            self.setAttribute(Qt.WA_StyledBackground, True)
        if state in (State.RESIZE, State.DEFAULT):
            self.setGeometry(
                self.x_pos * parent_w,
                self.y_pos * parent_h,
                self.w * parent_w,
                self.h * parent_h
            )
            self.setStyleSheet(self._stylesheet())
            for i, widget in enumerate(self.widgets):
                cols = max(int(self.w * parent_w // (self.m * 0.25)), 1)
                rows = (i // cols)
                col = i % cols
                widget.w = 0.23
                widget.h = 0.25
                widget.x_pos = (col * 0.25) + 0.02
                widget.y_pos = (rows * 0.25) + 0.02
                widget.cupdate(State.RESIZE)
                widget.raise_()

    def _stylesheet(self):
        return f"""
            QFrame {{
                background-color: {self.background_color};
                border-radius: {self.m*0.04}px;
            }}
        """
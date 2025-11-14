import csv
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFrame, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QHeaderView,
    QAbstractScrollArea, QScrollArea
)
from PySide6.QtCore import Qt
from filemanagment import Result
import color_palette as cp

class CSVDisplay(QFrame):
    """Widget for displaying CSV data in a table."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = QTableWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setStyleSheet(self._stylesheet())
        
    def load_csv(self, path: str):
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = list(csv.reader(f))
                if not reader: return

                headers, rows = reader[0], reader[1:]
                self.table.setColumnCount(len(headers))
                self.table.setHorizontalHeaderLabels(headers)
                self.table.setRowCount(len(rows))

                for r, row in enumerate(rows):
                    for c, val in enumerate(row):
                        self.table.setItem(r, c, QTableWidgetItem(val))

                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        except FileNotFoundError:
            print(f"Error: CSV file not found at {path}")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def _stylesheet(self):
        return f"""
            QFrame {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {cp.BACKGROUND_DARK}, stop:1 {cp.CARD_SURFACE});
            }}
            QTableWidget {{
                background-color: {cp.CARD_SURFACE}; color: {cp.PRIMARY_TEXT}; gridline-color: {cp.BORDER_DIVIDER};
                selection-background-color: {cp.INFO_HIGHLIGHT}; selection-color: {cp.PRIMARY_TEXT};
                border: none; font-family: "Inter", "Roboto", sans-serif; font-size: 13px;
            }}
            QHeaderView::section {{
                background-color: {cp.BORDER_DIVIDER}; color: {cp.PRIMARY_TEXT}; font-weight: bold;
            }}
            QScrollBar:vertical {{ background: {cp.BACKGROUND_DARK}; width: 10px; margin: 0px; }}
            QScrollBar::handle:vertical {{ background: {cp.BORDER_DIVIDER}; }}
            QScrollBar::handle:vertical:hover {{ background: {cp.INFO_HIGHLIGHT}; }}
        """

class CSVEditWidget(QFrame):
    """Widget for editing a CSV file. This appears as a separate window."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.result = None
        self.setWindowTitle("CSV Editor")
        self.setMinimumSize(600, 400)
        
        # Main Layout
        layout = QHBoxLayout(self)
        self.setLayout(layout)

        # Left side for info and controls (can be expanded)
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(200)
        
        self.label = QLabel("Editing profile")
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.hide)
        
        left_layout.addWidget(self.label)
        left_layout.addStretch()
        left_layout.addWidget(self.close_button)
        
        # Right side for CSV table
        self.csv_display = CSVDisplay()
        
        layout.addWidget(left_panel)
        layout.addWidget(self.csv_display, 1) # Add stretch factor

    def set_result(self, result: Result):
        self.result = result
        self.label.setText(f"Editing profile {result.id}")
        if result.csv_path:
            self.csv_display.load_csv(result.csv_path)
        self.setWindowTitle(f"CSV Editor - Profile {result.id}")

class ResultShowcaseWidget(QPushButton):
    """A clickable card widget to showcase a single result profile."""
    def __init__(self, result: Result, parent=None):
        super().__init__(parent)
        self.result = result
        self.setMinimumHeight(120)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Top part with label and remove button
        top_layout = QHBoxLayout()
        self.label = QLabel(f"Profile {result.id}")
        self.remove_button = QPushButton("X")
        self.remove_button.setFixedSize(20, 20)
        
        top_layout.addWidget(self.label)
        top_layout.addStretch()
        top_layout.addWidget(self.remove_button)
        
        layout.addLayout(top_layout)
        layout.addStretch() # Pushes content to top

        self.setLayout(layout)
        self.setStyleSheet(self._stylesheet())

    def _stylesheet(self):
        style = cp.BUTTON_STYLES["secondary"]
        return f"""
            QPushButton {{
                background-color: {style["background"]};
                border: 1px solid {style["border"]};
                color: {style["text"]};
                border-radius: 5px;
                text-align: left;
                padding: 5px;
            }}
            QPushButton:hover {{ background-color: {style["hover"]}; }}
            QPushButton:pressed {{ background-color: {style["pressed"]}; }}
            
            QLabel {{
                background-color: transparent;
                color: {cp.PRIMARY_TEXT};
                border: none;
                font-weight: bold;
            }}
            
            QPushButton#remove_button {{
                /* A specific stylesheet for the remove button if needed */
            }}
        """

class CSVGrid(QWidget):
    """Grid for displaying multiple result showcases."""
    def __init__(self, results, parent=None):
        super().__init__(parent)
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_layout.addWidget(scroll_area)

        # Widget to hold the grid layout
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        scroll_area.setWidget(self.grid_container)

        self.results = []
        self.widgets: list[ResultShowcaseWidget] = []
        
        # A single edit widget, managed by the grid
        self.edit_widget = CSVEditWidget()
        self.edit_widget.hide()

        self.update_results(results)

    def update_results(self, results: list[Result]):
        self.results = results
        self._turn_results_into_widgets()

    def _clear_layout(self):
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.widgets.clear()

    def _turn_results_into_widgets(self):
        self._clear_layout()
        
        cols = 4 # Use a fixed number of columns for stability

        for i, result in enumerate(self.results):
            widget = ResultShowcaseWidget(result, self)
            widget.clicked.connect(lambda _, r=result: self.show_edit_widget(r))
            widget.remove_button.clicked.connect(lambda w=widget: self.remove_result(w))
            
            row, col = divmod(i, cols)
            self.grid_layout.addWidget(widget, row, col)
            self.widgets.append(widget)

    def show_edit_widget(self, result: Result):
        self.edit_widget.set_result(result)
        self.edit_widget.show()
        self.edit_widget.raise_()

    def remove_result(self, widget: ResultShowcaseWidget):
        # Find the result associated with the widget
        result_to_remove = widget.result
        self.results = [res for res in self.results if res.id != result_to_remove.id]
        
        # Optional: Add logic here to delete the profile files from disk
        # filemanagment.delete_profile(result_to_remove.id)
        
        self._turn_results_into_widgets()
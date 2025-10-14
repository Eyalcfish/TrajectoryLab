from enum import Enum
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFrame, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from mode_selection_widgets import PopUpButton, blankWidget 

DEBUG = True

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

    def resizeEvent(self, event):
        # Update children geometry manually
        for child in self.findChildren(QWidget):
            if hasattr(child, "resizeEvent"):
                # Optionally trigger cupdate or resizeEvent
                child.resizeEvent(event)
                if hasattr(child, "cupdate"):
                    child.cupdate(None)

        super().resizeEvent(event)

def load_popupbuttons(window):
    blank1 = blankWidget(-0.1, 0.2, 0.3, 0.1, parent=window, debug=DEBUG)
    blank2 = blankWidget(-0.1, 0.4, 0.3, 0.1, parent=window, debug=DEBUG)
    blank3 = blankWidget(-0.1, 0.6, 0.3, 0.1, parent=window, debug=DEBUG)

    button1 = PopUpButton(" Initial Settings", w = 0.5, h = 1, pop_offset=0.3, background_color="#71bcda", parent=blank1)
    button2 = PopUpButton(" CSVs", w = 0.5, h = 1, pop_offset=0.3, background_color="#58a9df", parent=blank2)
    button3 = PopUpButton("Function\n Generator", w = 0.5, h = 1, pop_offset=0.3, background_color="#2f1ec5", parent=blank3)

    button1.clicked.connect(lambda: set_current_window(0,button1,button2,button3))
    button2.clicked.connect(lambda: set_current_window(1,button2,button1,button3))
    button3.clicked.connect(lambda: set_current_window(2,button3,button2,button1))
    button1.pop_up(True)

def load_widgets(window):
    load_popupbuttons(window)

def set_current_window(val, button: PopUpButton, button_out1: PopUpButton, button_out2: PopUpButton):
    global current_window
    current_window = val

    button.pop_up(True)
    button_out1.pop_up(False)
    button_out2.pop_up(False)

if __name__ == "__main__":
    current_window = 0  

    app = QApplication([])

    window = MyWindow()
    window.resize(600, 400)

    load_widgets(window)

    window.show()
    app.exec()

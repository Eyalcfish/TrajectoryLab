from PySide6.QtWidgets import QMainWindow
from cwidgets import cWidget

class Window(QMainWindow):
    def __init__(self, name, size=(800, 600)):
        super().__init__()
        self.setWindowTitle(name)
        self.resize(*size)
        self.w, self.h = self.width(), self.height()
        self.cWidgets = []
        self.setStyleSheet("background-color: #000000;")

    def add_widget(self, cWidget: cWidget):
        self.cWidgets.append(cWidget)
        cWidget.adopt(self)

    def load_widget(self, cWidget: cWidget):
        cWidget.load(self.w, self.h)

    def load_widgets(self):
        for cWidget in self.cWidgets:
            self.load_widget(cWidget)

    def resizeEvent(self, event):
        self.w, self.h = self.width(), self.height()
        self.load_widgets()
        super().resizeEvent(event)
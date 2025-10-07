from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFrame, QWidget
from PySide6.QtCore import Qt
from cwidgets import cButton, cDrawer, cLabel, cPopUpButton, cWidget

from cwindow import Window

class MainWindow(Window):
    def __init__(self):
        super().__init__("Dynamic Layout Example", (800, 600))

        # img = cWidget(pos=(0,0),
        #                 size=(1,0.5),
        #                 stretch=True,
        #                 radius=10,
        #                 bg_color="#3498db",
        #                 border_color="#2980b9",
        #                 border_width=20,
        #                 parent=self
        #         )
        # self.add_widgets(img)

        # Activation area is a rectangle in fractional coordinates (x, y, width, height)
        engines_button = cPopUpButton(
            "Engines",
            parent=self,
            pos=(-0.7,0.15),
            text_size=15,
            activation_area=(0.3,1),
            pop_offset=(0.7, 0),
            self_dimensions=1,
            bg_color="#2c3e50",
            border_color="#34495e",
            border_width=10,
        )
        engines_button.clicked.connect(lambda: print("Engines button clicked!"))

        engines_results_button = cPopUpButton(
            "Engine Results",
            parent=self,
            pos=(-0.83,0.3),
            text_size=15,
            activation_area=(0.17,1),
            pop_offset=(0.83, 0),
            self_dimensions=1,
            bg_color="#2c3e50",
            border_color="#34495e",
            border_width=10,
        )
        engines_results_button.clicked.connect(lambda: print("Engines button clicked!"))

        poly_functions_button = cPopUpButton(
            "Poly Functions",
            parent=self,
            pos=(-0.83,0.45),
            text_size=15,
            activation_area=(0.17,1),
            pop_offset=(0.83, 0),
            self_dimensions=1,
            bg_color="#2c3e50",
            border_color="#34495e",
            border_width=10,
        )
        poly_functions_button.clicked.connect(lambda: print("Poly Functions button clicked!"))

        top_bar = cWidget(
            pos=(0,0),
            size=(1,0.1),
            stretch=True,
            bg_color="#c5600d",
            border_color="#96311f",
            border_width=20,
            clip_to_parent=True,
            parent=self
        )

        drawer = cDrawer(
            pos=(0.1,0.1),
            size=(0.8,0.8),
            stretch=True,
            bg_color="#18beca",
            radius=10,
            parent=self
        )

        drawer.lower()

        cbutton = cButton(
            "Click Me",
            parent=drawer,
            pos=(0,0),
            stretch=True,
            bg_color="#27ae60",
            text_color="#ffffff",
            hover_color="#2ecc71",
            pressed_color="#27ae60",
            radius=10,
            text_size=20,
            mode=cButton.MODE_FIXED_TEXT_SIZE
        )

        cbutton2 = cButton(
            "123123 Me2",
            parent=drawer,
            pos=(0.3,0),
            stretch=True,
            bg_color="#27ae60",
            text_color="#ffffff",
            hover_color="#2ecc71",
            pressed_color="#27ae60",
            radius=10,
            text_size=20,
            mode=cButton.MODE_FIXED_TEXT_SIZE
        )

        self.add_widgets(drawer)
        drawer.add_widget(cbutton)
        drawer.add_widget(cbutton2)
        cbutton.hide()
        # self.add_widgets(top_bar)
        self.add_widgets(engines_button)
        self.add_widgets(engines_results_button)
        self.add_widgets(poly_functions_button)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFrame, QWidget
from PySide6.QtCore import Qt
from cwidgets import cButton, cDrawer, cLabel, cPopUpButton, cWidget, Window
from mywidgets import WidgetWithThreeDots


class MainWindow(Window):
    def __init__(self):
        super().__init__("Dynamic Layout Example", (800, 600))

        engines_button = cPopUpButton(
            parent=None,
            text="Engines",   # ✅ pass as keyword
            pos_mode=cWidget.MOVE_BY_SELF_FRACTION,
            pos=(-0.7, 0.15),
            size=(0.15, 0.05),
            bg_color="#2c3e50",
            self_dimensions=1,
            border_color="#34495e",
            border_width=10,
            pop_offset=(0.7, 0),
        )


        engines_results_button = cPopUpButton(
            text = "Engine Results",
            pos_mode=cWidget.MOVE_BY_SELF_FRACTION,
            pos=(-0.7,0.3),
            size=(0.15,0.05),
            pop_offset=(0.7, 0),
            self_dimensions=1,
            bg_color="#2c3e50",
            border_color="#34495e",
            border_width=10,
        )
        engines_results_button.clicked.connect(lambda: print("Engines button clicked!"))

        poly_functions_button = cPopUpButton(
            text= "Poly Functions",         
            pos_mode=cWidget.MOVE_BY_SELF_FRACTION,
            pos=(-0.7,0.45),
            size=(0.15,0.05),
            pop_offset=(0.7, 0),
            self_dimensions=1,
            bg_color="#2c3e50",
            border_color="#34495e",
            border_width=10,
        )
        poly_functions_button.clicked.connect(lambda: print("Poly Functions button clicked!"))

        drawer: cDrawer = cDrawer(
            pos=(0.1,0.1),
            size=(0.8,0.8),
            stretch=True,
            bg_color="#18beca",
            radius=10,
            guard_width=0.03,
            items_per_row=1,
            items_per_column=1,
        )

        cbutton = cButton(
            text = "Click Me",
            pos=(0,0),
            size=(0.4,0.1),
            stretch=True,
            bg_color="#27ae60",
            text_color="#ffffff",
            hover_color="#2ecc71",
            pressed_color="#27ae60",
            radius=10,
        )

        cbutton2 = cButton(
            text="Click Me",
            pos=(0.3, 0),
            size=(0.4, 0.1),
            stretch=True,
            bg_color="#27ae60",
            text_color="#ffffff",
            hover_color="#2ecc71",
            pressed_color="#27ae60",
            radius=10,
        )

        cbutton3 = cButton(
            text="Click Me",
            pos=(0.3,0),
            size=(0.4,0.1),
            stretch=True,
            bg_color="#27ae60",
            text_color="#ffffff",
            hover_color="#2ecc71",
            pressed_color="#27ae60",
            radius=10,
        )
        cbutton4 = cButton(
            text=":",
            pos=(0.3,0),
            size=(0.4,0.1),
            stretch=False,
            bg_color="#27ae60",
            text_color="#ffffff",
            hover_color="#2ecc71",
            pressed_color="#27ae60",
            radius=100000,
        )

        custom = WidgetWithThreeDots(
            three_dots_size=(0.1,0.1),
            widget=cLabel(
                text="Custom Widget",
                pos=(0,0),
                size=(0.7,0.1),
                stretch=True,
                bg_color="#8e44ad",
                text_color="#ffffff",
                radius=10,
            ),
            bg_color="#e76d3c",
            pos=(0,0),
            size=(0.4,0.1),
            stretch=True,
            radius=10,

        )

        drawer.setMouseTracking(True)

        self.add_widget(drawer)
        drawer.add_widget(custom)

        self.add_widget(engines_button)
        self.add_widget(engines_results_button)
        self.add_widget(poly_functions_button)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

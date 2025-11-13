import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QStackedWidget, QLabel
from custom_widgets import State,BaseWidget, EventMixin
from mode_selection_widgets import SideBar, SideBarButton
from initial_settings_menu import InitialSettingsMenu
from csv_view_widgets import CSVGrid
from filemanagment import list_of_results
import color_palette as cp

# class testWidget(QWidget, EventMixin, QFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.x_pos = 0
#         self.y_pos = 0
#         self.w = 100
#         self.h = 100
#         self.parent_w = 0
#         self.parent_h = 0
#         self.m = 0

class MainWindow(QWidget):
    """Main window for the Trajectory Lab application."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trajectory Lab")
        self.setStyleSheet(f"background-color: {cp.BACKGROUND_STYLES['main_window']['color']};")
        self.resize(800, 600)
        
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Content area with QStackedWidget
        self.stacked_widget = QStackedWidget()
        self._populate_views()
        main_layout.addWidget(self.stacked_widget)

        # Set layout stretch factors
        main_layout.setStretchFactor(self.sidebar, 1)
        main_layout.setStretchFactor(self.stacked_widget, 9)

        self.setLayout(main_layout)
        self.set_current_window(0)

    def _create_sidebar(self):
        """Create the mode selection sidebar."""
        sidebar = SideBar(" Mode Selection ", parent=self)
        
        buttons_config = [
            (" Initial Settings ", True),
            (" CSV View ", False),
            (" Poly Functions ", False)
        ]
        
        self.sidebar_buttons = []
        for text, pressed in buttons_config:
            button = SideBarButton(text, pressed=pressed, parent=sidebar)
            sidebar.add_button(button)
            self.sidebar_buttons.append(button)

        self.sidebar_buttons[0].clicked.connect(lambda: self.set_current_window(0))
        self.sidebar_buttons[1].clicked.connect(lambda: self.set_current_window(1))
        self.sidebar_buttons[2].clicked.connect(lambda: self.set_current_window(2))
        
        return sidebar

    def _populate_views(self):
        """Load and initialize all UI widgets into the stacked widget."""
        self.initial_settings_menu = InitialSettingsMenu()
        self.csv_showcase = CSVGrid(
            results=list_of_results(include_output=False, include_settings=False)
        )
        
        # Placeholder for "Poly Functions"
        poly_functions_placeholder = QWidget()
        poly_functions_placeholder.setStyleSheet("background-color: #2c3e50;")

        self.stacked_widget.addWidget(self.initial_settings_menu)
        self.stacked_widget.addWidget(self.csv_showcase)
        self.stacked_widget.addWidget(poly_functions_placeholder)

    def set_current_window(self, index):
        """Switch between different views in the main window."""
        self.stacked_widget.setCurrentIndex(index)
        
        for i, button in enumerate(self.sidebar_buttons):
            button.set_pressed(i == index)

        if index == 1: # CSV View is selected
            self.csv_showcase.update_results(list_of_results(include_output=False, include_settings=False))



class App:
    """Main application class."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

    def run(self):
        """Show the main window and run the application."""
        self.window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    import threading
    app = App()
    app.run()

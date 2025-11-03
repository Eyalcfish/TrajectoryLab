from enum import Enum
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFrame, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from custom_widgets import EventMixin, State, fit_text_to_widget
from mode_selection_widgets import blankWidget, sideBar, sideBarButton
from settings_menu_widgets import SettingWidget, SettingWidgetContainer
from initial_settings_menu import InitialSettingsMenu
from csv_view_widgets import ResultShowcaseWidget,CSVGrid
from filemanagment import Result, list_of_results
DEBUG = True

# 🎨 Core Colors

# Primary (Blue): #3B82F6 — strong, modern blue (like Tailwind’s)
# Primary Light: #60A5FA — hover/highlight version
# Primary Dark: #1E40AF — pressed or dark-theme accent

# ⚫ Neutrals / Background

# Background (Dark): #0D0D0D — near-black, not pure (#000) to avoid harsh contrast
# Card / Surface: #1A1A1A — slightly lighter for UI separation
# Border / Divider: #2C2C2C

# ⚪ Text & Highlights

# Primary Text: #FFFFFF — pure white for clarity
# Secondary Text: #B0B0B0 — muted gray for lower emphasis
# Accent White (on blue): #E6F0FF — softer white that blends well with blue

# 🔵 Optional Accent Shades

# Info / Highlight: #38BDF8 — light cyan tint for hover effects
# Success: #22C55E — green that fits blue contrast
# Error: #EF4444 — bright red for alerts

initial_settings_menu = None
csv_showcase = None
current_window = 1

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
                    child.cupdate(State.RESIZE)

        super().resizeEvent(event)

def load_widgets(window):
    global initial_settings_menu, csv_showcase
    csv_showcase = CSVGrid(x = 0.15, y=0.05, w=0.8, h=0.9, results=list_of_results(include_output=False, include_settings=False), parent=window, background_color="#1A1A1A")
    sidebar = sideBar(" Mode Selection ", w=0.1, pos="left", parent=window)
    sidebarButton1 = sideBarButton(" Initial Settings ", pressed= True, x=0.05, h=0.06, parent=sidebar)
    sidebar.add_button(sidebarButton1)
    sidebarButton2 = sideBarButton(" CSV View ", pressed = False, x=0.05, h=0.06, parent=sidebar)
    sidebar.add_button(sidebarButton2)
    sidebarButton3 = sideBarButton(" Poly Functions ", pressed = False, x=0.05, h=0.06, parent=sidebar)
    sidebar.add_button(sidebarButton3)
    sidebarButton1.clicked.connect(lambda: set_current_window(0, sidebarButton1, sidebarButton2, sidebarButton3))
    sidebarButton2.clicked.connect(lambda: set_current_window(1, sidebarButton2, sidebarButton1, sidebarButton3))
    sidebarButton3.clicked.connect(lambda: set_current_window(2, sidebarButton3, sidebarButton1, sidebarButton2))
    initial_settings_menu = InitialSettingsMenu(parent = window)
    csv_showcase.show()
    initial_settings_menu.hide()

def set_current_window(val, button: sideBarButton, button_out1: sideBarButton, button_out2: sideBarButton):
    global current_window, initial_settings_menu, csv_showcase
    current_window = val
    button.pressed = True
    button_out1.pressed = False
    button_out2.pressed = False
    button.cupdate(State.REPAINT)
    button_out1.cupdate(State.REPAINT)
    button_out2.cupdate(State.REPAINT)
    if current_window == 0:
        initial_settings_menu.show()
        csv_showcase.hide()
    else:
        initial_settings_menu.hide()
        csv_showcase.show()

if __name__ == "__main__":
    current_window = 0  

    app = QApplication([])

    window = MyWindow()
    window.setStyleSheet("background-color: #1A1A1A;")
    window.resize(600, 400)

    load_widgets(window)

    window.show()
    app.exec()

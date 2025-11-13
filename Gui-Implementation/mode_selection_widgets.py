from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from custom_widgets import EventMixin, State, fit_text_to_widget
import color_palette as cp

class SideBarButton(QPushButton, EventMixin):
    """A custom button for the sidebar."""
    def __init__(self, text, pressed=False, parent=None):
        super().__init__(text, parent)
        self._pressed = pressed
        self.set_pressed(self._pressed)

    def set_pressed(self, is_pressed):
        self._pressed = is_pressed
        self.setStyleSheet(self._stylesheet(pressed=self._pressed))
        self.update()

    def cupdate(self, state: State):
        # This is kept for EventMixin compatibility, but we only care about clicks
        if state == State.CLICKED:
            # The logic is handled by the parent now
            pass

    def _stylesheet(self, pressed):
        style = cp.BUTTON_STYLES["primary"]
        padding = 4
        border_radius = 5
        
        if pressed:
            return f"""
                QPushButton {{
                    background-color: {cp.INFO_HIGHLIGHT};
                    border: 1px solid {style["border"]};
                    color: {style["text"]};
                    border-radius: {border_radius}px;
                    padding: {padding}px;
                    text-align: left;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: {style["background"]};
                    border: none;
                    color: {style["text"]};
                    border-radius: {border_radius}px;
                    padding: {padding}px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {style["hover"]};
                }}
                QPushButton:pressed {{
                    background-color: {style["pressed"]};
                }}
            """

class SideBar(QWidget):
    """A sidebar widget for mode selection."""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(self._stylesheet())

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 10, 5, 10)
        self.layout.setSpacing(5)
        self.layout.setAlignment(Qt.AlignTop)

        # Title
        self.title_label = QLabel(text)
        self.title_label.setStyleSheet(f"color: {cp.PRIMARY_TEXT}; font-weight: bold; padding-bottom: 10px;")
        self.layout.addWidget(self.title_label)

        self.buttons: list[SideBarButton] = []
        self.setLayout(self.layout)

    def add_button(self, button: SideBarButton):
        self.buttons.append(button)
        self.layout.addWidget(button)

    def _stylesheet(self):
        return f"""
            background-color: {cp.BACKGROUND_DARK}; 
            border-right: 1px solid {cp.BACKGROUND_STYLES["sidebar"]["color"]};
        """
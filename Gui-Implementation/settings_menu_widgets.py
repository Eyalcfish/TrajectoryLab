from PySide6.QtWidgets import QPushButton, QWidget, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt
from custom_widgets import EventMixin, fit_text_to_widget
import color_palette as cp

class SettingWidget(QWidget):
    """Widget for a single setting with a label and line edit."""
    def __init__(self, default_value, setting_name="Setting", parent=None):
        super().__init__(parent)
        
        self.lineedit = QLineEdit()
        self.lineedit.setValidator(QDoubleValidator())
        self.lineedit.setPlaceholderText(str(default_value))
        
        self.label = QLabel(setting_name)
        
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        
        self.setStyleSheet(self._stylesheet())

    def _stylesheet(self):
        return f"""
            QLabel {{
                color: {cp.SECONDARY_TEXT};
                padding-right: 10px;
            }}
            QLineEdit {{
                background-color: {cp.CARD_SURFACE};
                color: {cp.PRIMARY_TEXT};
                border: none;
                border-bottom: 1px solid {cp.BORDER_DIVIDER};
                padding: 4px;
            }}
            QLineEdit:focus {{
                border-bottom: 1px solid {cp.PRIMARY_BLUE};
            }}
        """

class SettingWidgetContainer(QFrame):
    """Container for multiple SettingWidgets."""
    def __init__(self, category_name="Category", parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFrameShape(QFrame.StyledPanel)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)
        
        self.label = QLabel(category_name)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        self.settings: list[SettingWidget] = []
        self.setLayout(self.layout)
        self.setStyleSheet(self._stylesheet())

    def add_setting(self, setting: SettingWidget):
        self.settings.append(setting)
        self.layout.addWidget(setting)

    def _stylesheet(self):
        return f"""
            QFrame {{
                background-color: {cp.CARD_SURFACE};
                border-radius: 5px;
            }}
            QLabel {{
                color: {cp.PRIMARY_BLUE};
                font-weight: bold;
                padding-bottom: 5px;
            }}
        """

class CSVGenerateButton(QPushButton):
    """Button to generate a CSV file, showing progress."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.original_text = text
        self.progress = 0
        self.setStyleSheet(self._stylesheet())
        self.setText(f"{self.original_text} (0.0%)")

    def set_progress(self, percentage):
        """Update the button's text to show progress."""
        self.progress = percentage
        self.setText(f"{self.original_text} ({self.progress:.1%})")
        # We need to re-apply the stylesheet for the gradient to update
        self.setStyleSheet(self._stylesheet())

    def _stylesheet(self):
        style = cp.BUTTON_STYLES["success"]
        
        return f"""
            QPushButton {{
                background-color: {style["background"]};
                border: none;
                color: {style["text"]};
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {style["hover"]};
            }}
            QPushButton:pressed {{
                background-color: {style["pressed"]};
            }}
            QPushButton:disabled {{
                background-color: {style["background"]};
            }}
        """

class ProfileSelector(QLineEdit):
    """Line edit for profile selection."""
    def __init__(self, default_value=None, parent=None):
        super().__init__(parent)
        if default_value is not None:
            self.setPlaceholderText(str(default_value))
        self.setStyleSheet(self._stylesheet())

    def _stylesheet(self):
        return f"""
            QLineEdit {{
                background-color: {cp.CARD_SURFACE}; color: {cp.PRIMARY_TEXT};
                border: none; border-radius: 8px; padding: 5px;
                border-bottom: 1px solid {cp.BORDER_DIVIDER};
            }}
            QLineEdit:focus {{ border-bottom: 1px solid {cp.PRIMARY_BLUE}; }}
        """

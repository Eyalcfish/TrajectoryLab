from enum import Enum
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QColor, QPainter, QBrush, QFontMetrics, QFont
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, Qt, QTimer

def fit_text_to_widget(widget, text=None, padding=6):
    """
    Automatically adjust font size so 'text' fits exactly inside the widget.
    
    Args:
        widget: Any QWidget with setText() and setFont() methods.
        text: Optional; if None, uses widget.text().
        padding: Pixel margin inside the widget to keep text from touching edges.
    """
    if text is None:
        return  # widget has no text

    rect = widget.contentsRect()
    available_w = rect.width() - padding * 2
    available_h = rect.height() - padding * 2

    if available_w <= 0 or available_h <= 0:
        return

    font = widget.font()
    size = 1
    fm = QFontMetrics(font)

    # Increase font size until text doesn't fit
    while True:
        font.setPointSize(size)
        fm = QFontMetrics(font)
        if fm.horizontalAdvance(text) > available_w or fm.height() > available_h:
            break
        size += 1

    # Step back one size
    font.setPointSize(max(size - 1, 1))
    widget.setFont(font)

class State(Enum):
    DEFAULT = 0
    RESIZE = 1
    ENTER_HOVER = 2
    LEAVE_HOVER = 3
    CLICKED = 4
    REPAINT = 5
    CHILD_ADDED = 6

class EventMixin:
    """Mixin that calls cupdate(State) for standard events."""
    def enterEvent(self, event):
        if hasattr(self, "cupdate"):
            self.cupdate(State.ENTER_HOVER)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if hasattr(self, "cupdate"):
            self.cupdate(State.LEAVE_HOVER)
        super().leaveEvent(event)

    def clickEvent(self, event):
        if hasattr(self, "cupdate"):
            self.cupdate(State.CLICKED)
        super().clickEvent(event)

    def resizeEvent(self, event):
        if hasattr(self, "cupdate"):
            self.cupdate(State.RESIZE)
        super().resizeEvent(event)
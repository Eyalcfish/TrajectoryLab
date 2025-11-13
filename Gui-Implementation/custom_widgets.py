from enum import Enum
from PySide6.QtWidgets import QWidget,QFrame
from PySide6.QtGui import QFontMetrics

class State(Enum):
    """Enumeration for widget states."""
    DEFAULT = 0
    RESIZE = 1
    ENTER_HOVER = 2
    LEAVE_HOVER = 3
    CLICKED = 4
    REPAINT = 5
    CHILD_ADDED = 6

def fit_text_to_widget(widget, text=None, padding=6):
    """
    Automatically adjust font size so 'text' fits exactly inside the widget.
    
    Args:
        widget: Any QWidget with setText() and setFont() methods.
        text: Optional; if None, uses widget.text().
        padding: Pixel margin inside the widget to keep text from touching edges.
    """
    if text is None:
        text = widget.text()

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

class EventMixin:
    """Mixin that calls cupdate(State) for standard events."""
    def enterEvent(self, event):
        self.cupdate(State.ENTER_HOVER)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.cupdate(State.LEAVE_HOVER)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.cupdate(State.CLICKED)
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        self.cupdate(State.RESIZE)
        super().resizeEvent(event)

class BaseFrame(QFrame, EventMixin):
    """Base class for custom widgets providing common functionality."""
    def __init__(self, parent=None, x=0, y=0, w=1, h=1):
        super().__init__(parent)
        self.x_pos = x
        self.y_pos = y
        self.w = w
        self.h = h
        self.parent_w = 0
        self.parent_h = 0
        self.m = 0

    def cupdate(self, state: State):
        """
        Custom update logic for the widget based on its state.
        This method should be overridden by subclasses.
        """
        if self.parent():
            self.parent_w = self.parent().width()
            self.parent_h = self.parent().height()
            self.m = min(self.w * self.parent_w, self.h * self.parent_h)

        if state in (State.RESIZE, State.DEFAULT):
            self.setGeometry(
                self.x_pos * self.parent_w,
                self.y_pos * self.parent_h,
                self.w * self.parent_w,
                self.h * self.parent_h
            )
    
    def _stylesheet(self, state=None):
        """
        Returns the stylesheet for the widget.
        This method should be overridden by subclasses.
        """
        return ""


class BaseWidget(QWidget, EventMixin):
    """Base class for custom widgets providing common functionality."""
    def __init__(self, parent=None, x=0, y=0, w=1, h=1):
        super().__init__(parent)
        self.x_pos = x
        self.y_pos = y
        self.w = w
        self.h = h
        self.parent_w = 0
        self.parent_h = 0
        self.m = 0

    def cupdate(self, state: State):
        """
        Custom update logic for the widget based on its state.
        This method should be overridden by subclasses.
        """
        if self.parent():
            self.parent_w = self.parent().width()
            self.parent_h = self.parent().height()
            self.m = min(self.w * self.parent_w, self.h * self.parent_h)

        if state in (State.RESIZE, State.DEFAULT):
            self.setGeometry(
                self.x_pos * self.parent_w,
                self.y_pos * self.parent_h,
                self.w * self.parent_w,
                self.h * self.parent_h
            )
    
    def _stylesheet(self, state=None):
        """
        Returns the stylesheet for the widget.
        This method should be overridden by subclasses.
        """
        return ""

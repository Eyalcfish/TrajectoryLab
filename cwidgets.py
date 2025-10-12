from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFrame, QWidget, QFrame
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QFontMetrics
from PySide6.QtCore import Qt, Signal, QRect, QRectF, QPointF

def max_font_size(text: str, font: QFont, width: int, height: int) -> int:
    if not text or width <= 0 or height <= 0:
        return 1

    lines = text.splitlines() or [text]

    low, high = 1, 500
    best = low

    while low <= high:
        mid = (low + high) // 2
        f = QFont(font)
        f.setPixelSize(mid)
        fm = QFontMetrics(f)

        text_width = max(fm.horizontalAdvance(line) for line in lines)
        text_height = fm.lineSpacing() * len(lines)

        if text_width <= width and text_height <= height:
            best = mid
            low = mid + 1
        else:
            high = mid - 1

    return best

def scale_color(color: QColor, factor: float) -> QColor:
    r = min(int(color.red() * factor), 255)
    g = min(int(color.green() * factor), 255)
    b = min(int(color.blue() * factor), 255)
    return QColor(r, g, b, color.alpha())

def add_colors(c1: QColor, c2: QColor) -> QColor:
    r = min(c1.red() + c2.red(), 255)
    g = min(c1.green() + c2.green(), 255)
    b = min(c1.blue() + c2.blue(), 255)
    a = min(c1.alpha() + c2.alpha(), 255)
    return QColor(r, g, b, a)

class cWidget(QWidget):
    MOVE_BY_PIXEL = 0
    MOVE_BY_FRACTION = 1
    MOVE_BY_SELF_FRACTION = 2
    SIZE_BY_FRACTION = 0
    SIZE_BY_PIXEL = 1

    def __init__(self, parent=None, *, bg_color="#FFFFFF", radius=0, border_color=None,
                 border_width=0, pos=(0,0), size=(0,0), stretch=False,
                 pos_mode=MOVE_BY_FRACTION, clip_to_parent=True, self_dimensions=0,
                 size_type=SIZE_BY_FRACTION):
        super().__init__(parent)
        self.cpos = pos
        self.pos_mode = pos_mode
        self.csize = size
        self.stretch = stretch
        self.clip_to_parent = clip_to_parent
        self.bg_color = QColor(bg_color)
        self.radius = radius
        self.border_color = QColor(border_color) if border_color else None
        self.border_width = border_width
        self.self_dimensions = self_dimensions
        self.size_type = size_type
        self.setAutoFillBackground(True)
        self.m = 0
        self.parent_w = 0
        self.parent_h = 0


    def adopt(self, parent: QWidget):
        if parent:
            self.setParent(parent)
            self.parent_w = parent.width()
            self.parent_h = parent.height()
            self.load(parent.width(), parent.height())

    def paintEvent(self, event):
        radius = int(self.radius * 0.001 * self.m)
        border_width = int(self.border_width * 0.001 * self.m)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(self.bg_color))

        if self.border_color and border_width > 0:
            pen = QPen(self.border_color, border_width)
        else:
            pen = QPen(Qt.NoPen)

        painter.setPen(pen)

        rect = self.rect()
        if border_width > 0:
            offset = border_width // 2
            rect = rect.adjusted(offset, offset, -offset, -offset)

        if self.radius > 0:
            painter.drawRoundedRect(rect, radius, self.radius)
        else:
            painter.drawRect(rect)
        return painter

    def move(self, x, y, mode=MOVE_BY_FRACTION):
        self.pos_mode = mode
        self.cpos = (x, y)
        self.load(self.parent_w, self.parent_h)

    def setSize(self, w, h):
        self.csize = (w, h)
        self.load()

    def load(self, parent_w=None, parent_h=None):
        self.parent_w = parent_w if parent_w is not None else self.parent().width()
        self.parent_h = parent_h if parent_h is not None else self.parent().height()
        self.m = min(self.parent_w, self.parent_h)

        x = int(self.parent_w * self.cpos[0])
        y = int(self.parent_h * self.cpos[1])

        if self.size_type == cWidget.SIZE_BY_FRACTION:
            width = int(self.parent_w * self.csize[0])
            height = int(self.parent_h * self.csize[1])
        else:
            width = int(self.csize[0])
            height = int(self.csize[1])

        if not self.stretch:
            width = min(width,height)
            height = min(width,height)

        if self.clip_to_parent:
            if x < 0:
                width = max(0, width + x)  # reduce width if partially off left
                x = 0
            if y < 0:
                height = max(0, height + y)
                y = 0
            width = min(width, self.parent_w - x)
            height = min(height, self.parent_h - y)

        x = int(width * self.cpos[0])
        y = int(height * self.cpos[1])
        if self.pos_mode == cWidget.MOVE_BY_PIXEL:
            x = int(self.cpos[0])
            y = int(self.cpos[1])
        elif self.pos_mode == cWidget.MOVE_BY_SELF_FRACTION:
            if self.self_dimensions == 1 or self.self_dimensions == 3:
                x = int(width * self.cpos[0])
            if self.self_dimensions >= 2:
                y = int(height * self.cpos[1])

        self.w = width
        self.h = height

        self.setGeometry(x, y, width, height)
        self.update()


class Window(QMainWindow):
    def __init__(self, name="Window", size=(800, 600), *args, **kwargs):
        super().__init__(*args, **kwargs)  # only pass parent/flags if needed
        self.setWindowTitle(name)          # set title separately
        self.resize(*size)                 # set size separately
        self.w, self.h = self.width(), self.height()
        self.cWidgets = []
        self.setStyleSheet("background-color: #000000;")

    def add_widget(self, widget: cWidget):
        self.cWidgets.append(widget)
        widget.adopt(self)
        self.load_widgets()

    def load_widget(self, widget: cWidget):
        widget.load(self.w, self.h)

    def load_widgets(self):
        for widget in self.cWidgets:
            self.load_widget(widget)

    def resizeEvent(self, event):
        self.w, self.h = self.width(), self.height()
        self.load_widgets()
        super().resizeEvent(event)

class cLabel(cWidget):
    MODE_FRACTIONAL_SIZE = 0
    MODE_FIXED_TEXT_SIZE = 1

    def __init__(self, parent=None, *, text="", text_color="#000000", **kwargs):
        super().__init__(parent, **kwargs)
        self.text = text
        self.text_color = QColor(text_color)
        self.alignment = Qt.AlignCenter
        self.cfont = QFont("Arial", 12)
        self.cfont.setPixelSize(3)
        self.m = 0

    def load(self, parent_w=None, parent_h=None):
        self.parent_w = parent_w if parent_w is not None else self.parent().width()
        self.parent_h = parent_h if parent_h is not None else self.parent().height()
        self.m = min(self.parent_w, self.parent_h)

        if self.size_type == cWidget.SIZE_BY_FRACTION:
            width = int(self.parent_w * self.csize[0])
            height = int(self.parent_h * self.csize[1])
        else:
            width = int(self.csize[0])
            height = int(self.csize[1])

        if not self.stretch:
            width = min(width,height)
            height = min(width,height)

        font_size = max_font_size(self.text, self.cfont, width-self.border_width, height-self.border_width)
        self.cfont.setPixelSize(font_size)

        x = int(self.parent_w * self.cpos[0])
        y = int(self.parent_h * self.cpos[1])
        if self.pos_mode == cWidget.MOVE_BY_PIXEL:
            x = int(self.cpos[0])
            y = int(self.cpos[1])
        elif self.pos_mode == cWidget.MOVE_BY_SELF_FRACTION:
            if self.self_dimensions == 1 or self.self_dimensions == 3:
                x = int(width * self.cpos[0])
            if self.self_dimensions >= 2:
                y = int(height * self.cpos[1])
        self.setGeometry(x, y, width, height)

        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.text_color)

        painter.setFont(self.cfont)
        painter.drawText(self.rect(), self.alignment, self.text)

class cButton(cLabel):
    clicked = Signal()

    def __init__(self, *args, hover_color=None, pressed_color=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.normal_color = QColor(self.bg_color)
        self.hover_color = QColor(hover_color) if hover_color else self.normal_color.lighter(110)
        self.pressed_color = QColor(pressed_color) if pressed_color else self.normal_color.darker(110)
        self._pressed = False
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.bg_color = self.hover_color
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.bg_color = self.normal_color
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = True
            self.bg_color = self.pressed_color
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._pressed:
            self._pressed = False
            self.bg_color = self.hover_color
            self.update()
            # Only emit clicked if mouse release is inside the widget
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()
        super().mouseReleaseEvent(event)

class cPopUpButton(cButton):
    def __init__(self, *args, pop_offset=(0.05, 0), **kwargs):
        super().__init__(*args, **kwargs)
        self.pop_offset = pop_offset
        self._hovered = False
        self.original_pos = self.cpos


    def adopt(self, parent: QWidget):
        if parent:
            self.setParent(parent)
            self.parent_w = parent.width()
            self.parent_h = parent.height()
            self.load(parent.width(), parent.height())
            parent.setMouseTracking(True)
            parent.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == event.Type.MouseMove and self.parentWidget() == watched:
            w_area = int(self.width()-self.pop_offset[0]*self.width())
            h_area = int(self.height()-self.pop_offset[1]*self.height())
            pos_x = self.original_pos[0]*self.parentWidget().width()
            if self.self_dimensions == 1 or self.self_dimensions == 3:
                pos_x = self.original_pos[0]*self.width()
            pos_y = self.original_pos[1]*self.parentWidget().height()
            if self.self_dimensions >= 2:
                pos_y = self.original_pos[1] * self.height()
            area_rect = QRect(pos_x+self.pop_offset[0]*self.width(), pos_y+self.pop_offset[1]*self.height(), w_area, h_area)

            if area_rect.contains(event.position().toPoint()):
                self._activate_hover(event)
            else:
                widget_rect = self.geometry()
                if not widget_rect.contains(event.position().toPoint()):
                    self._deactivate_hover(event)

        return super().eventFilter(watched, event)

    def _activate_hover(self, event):
        if not self._hovered:
            self._hovered = True
            self.cpos = (self.original_pos[0] + self.pop_offset[0],
                         self.original_pos[1] + self.pop_offset[1])
            if self.parentWidget():
                self.load(self.parentWidget().width(), self.parentWidget().height())

    def _deactivate_hover(self, event):
        if self._hovered:
            self._hovered = False
            self.cpos = self.original_pos
            if self.parentWidget():
                self.load(self.parentWidget().width(), self.parentWidget().height())

class ccontainerWidget(cWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets: list[cWidget] = []
        self.w = 0
        self.h = 0

    def adopt(self, parent: QWidget):
        if parent:
            self.setParent(parent)
            self.parent_w = parent.width()
            self.parent_h = parent.height()
            self.load(self.parent_w, self.parent_h)
            self.w, self.h = self.width(), self.height()
            parent.setMouseTracking(True)

    def add_widget(self, widget: cWidget):
        self.widgets.append(widget)
        self.load(self.parent_w, self.parent_h)
        widget.adopt(self)
        self.load_widgets()

    def load_widgets(self):
        for widget in self.widgets:
            widget.load(self.w, self.h)

    def resizeEvent(self, event):
        self.load(self.parent_w, self.parent_h)
        self.load_widgets()
        super().resizeEvent(event)
        
class cDrawer(ccontainerWidget):
    def __init__(self, *args, guard_width=0, guard_color="#ffffff", guard_opacity=0.1,
                 items_per_row=3, items_per_column=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.guard_width = guard_width
        self.items_per_row = items_per_row
        self.items_per_column = items_per_column
        self.guard_opacity = guard_opacity
        self.guard_color = QColor(guard_color)

    def paintEvent(self, event):
        painter = super().paintEvent(event)

        guard_m = self.guard_width * min(self.width(), self.height())
        color = add_colors(scale_color(self.guard_color, self.guard_opacity), QColor(self.bg_color))


        x = 0
        for _ in range(self.items_per_row+1):
            painter.fillRect(x,0, guard_m, self.height(), color)
            x += (1/self.items_per_row)*self.width() - guard_m/2
        y = 0
        for _ in range(self.items_per_column+1):
            painter.fillRect(0,y, self.width(), guard_m, color)
            y += (1/self.items_per_column)*self.height() - guard_m/2
        # painter.fillRect(0, self.height() - guard_h, self.width(), guard_h, color)
        # painter.fillRect(0, 0, guard_w, self.height(), color)
        # painter.fillRect(self.width() - guard_w, 0, guard_w, self.height(), color)

        painter.end()

    def add_widget(self, widget: cWidget):
        self.widgets.append(widget)

        widget.setParent(self)
        widget.parent_h = self.height()
        widget.parent_w = self.width()
        self.load_widgets()

    def load_widgets(self):
        self.guard_m = self.guard_width * min(self.width(), self.height())
        x_offset = self.guard_m
        y_offset = self.guard_m
        i = 0
        for widget in self.widgets:
            widget.move(x_offset, y_offset, cWidget.MOVE_BY_PIXEL)
            x_offset += (1/self.items_per_row)*self.width() - self.guard_m/2
            widget.self_dimensions = 0
            widget.size_type = cWidget.SIZE_BY_PIXEL
            widget.setSize((1/self.items_per_row)*self.width() - self.guard_m, (1/self.items_per_column)*self.height() - self.guard_m*1.5)
            i += 1
            if i % self.items_per_row == 0:
                x_offset = self.guard_m
                y_offset += (1/self.items_per_column)*self.height() - self.guard_m/2     
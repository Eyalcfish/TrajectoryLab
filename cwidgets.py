from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFrame, QWidget, QFrame 
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QFontMetrics
from PySide6.QtCore import Qt, Signal, QRect



class cWidget(QWidget):
    MOVE_BY_PIXEL = 0
    MOVE_BY_FRACTION = 1
    MOVE_BY_SELF_FRACTION = 2
    def __init__(self, bg_color="#FFFFFF", radius=0, border_color=None, border_width=0,
                 pos=(0,0), size=(0,0), stretch=False, pos_mode=MOVE_BY_FRACTION, clip_to_parent=True, self_dimensions=0):
        super().__init__()
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

    def move(self, x, y, mode=MOVE_BY_FRACTION):
        self.pos_mode = mode
        self.cpos = (x, y)
        self.load(self.parent_w, self.parent_h)

    def load(self, w, h):
        self.parent_w = w
        self.parent_h = h
        self.m = min(w, h)

        x = int(w * self.cpos[0])
        y = int(h * self.cpos[1])

        if self.stretch:
            width = int(w * self.csize[0])
            height = int(h * self.csize[1])
        else:
            width = int(self.m * self.csize[0])
            height = int(self.m * self.csize[1])

        if self.clip_to_parent:
            if x < 0:
                width = max(0, width + x)  # reduce width if partially off left
                x = 0
            if y < 0:
                height = max(0, height + y)
                y = 0
            width = min(width, w - x)
            height = min(height, h - y)

        x = int(width * self.cpos[0])
        y = int(height * self.cpos[1])
        if self.pos_mode == cWidget.MOVE_BY_PIXEL:
            x = int(self.cpos[0])
            y = int(self.cpos[1])
            print(x)
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
    def __init__(self, name, size=(800, 600)):
        super().__init__()
        self.setWindowTitle(name)
        self.resize(*size)
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

    def __init__(self, text="", bg_color="#FFFFFF", radius=0, border_color=None, border_width=0,
                 pos=(0,0), size=(0,0), stretch=False, pos_mode=cWidget.MOVE_BY_FRACTION, text_color="#000000",
                 text_size=None, clip_to_parent= False, self_dimensions=0, mode=MODE_FIXED_TEXT_SIZE):
        super().__init__(bg_color, radius, border_color, border_width, pos, size, stretch, pos_mode=pos_mode, clip_to_parent=clip_to_parent, self_dimensions=self_dimensions)
        self.text = text
        self.text_color = QColor(text_color)
        self.font = QFont()
        self.alignment = Qt.AlignCenter
        self.mode = mode
        self.text_size = text_size if text_size < 1 or text_size is None else 12
        self.m = 0

    def load(self, parent_w, parent_h):
        self.m = min(parent_w, parent_h)

        if self.mode == self.MODE_FRACTIONAL_SIZE:
            width = int(self.csize[0] * parent_w)
            height = int(self.csize[1] * parent_h)
        else:
            self.font.setPixelSize(int(self.text_size * self.m / 200))
            fm = QFontMetrics(self.font)
            width = fm.horizontalAdvance(self.text) + 10
            height = fm.height() + 4

        x = int(width * self.cpos[0])
        y = int(height * self.cpos[1])
        if self.pos_mode == cWidget.MOVE_BY_PIXEL:
            x = int(self.cpos[0])
            y = int(self.cpos[1])
            print(x)
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

        if self.mode == self.MODE_FRACTIONAL_SIZE:
            self.font.setPixelSize(int(self.m * 0.08))  # scale with min dimension
        else:
            self.font.setPixelSize(int(self.text_size * self.m / 200))  # scale with min dimension

        painter.setFont(self.font)
        painter.drawText(self.rect(), self.alignment, self.text)

class cButton(cLabel):
    clicked = Signal()

    def __init__(self, text="", bg_color="#FFFFFF", radius=5,
                 border_color=None, border_width=0, pos=(0,0), size=(0,0), stretch=False,
                 pos_mode=cWidget.MOVE_BY_FRACTION,
                 text_color="#000000", hover_color=None, pressed_color=None,
                 text_size=None, clip_to_parent=False, self_dimensions=0, mode=cLabel.MODE_FIXED_TEXT_SIZE):
        super().__init__(text=text, bg_color=bg_color, radius=radius,
                         border_color=border_color, border_width=border_width,
                         pos=pos, size=size, stretch=stretch, pos_mode=pos_mode,
                         text_color=text_color, text_size=text_size, clip_to_parent=clip_to_parent, self_dimensions=self_dimensions, mode=mode)

        self.normal_color = QColor(bg_color)
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
    def __init__(self, text="", bg_color="#FFFFFF", radius=0,
                 border_color=None, border_width=0, pos=(0,0), size=(0,0), stretch=False, pos_mode=cWidget.MOVE_BY_FRACTION,
                 text_color="#000000", hover_color=None, pressed_color=None,
                 text_size=None, self_dimensions=0, clip_to_parent=True, mode=cButton.MODE_FIXED_TEXT_SIZE,
                 pop_offset=(0.05,0),  activation_area=None):
        """
        activation_area: (x, y, width, height) in fractional parent coordinates
        pop_offset: fraction of parent size to move when popped
        """
        super().__init__(text=text, bg_color=bg_color, radius=radius,
                         border_color=border_color, border_width=border_width,
                         pos=pos, size=size, stretch=stretch, 
                         text_color=text_color, hover_color=hover_color,
                         pressed_color=pressed_color, pos_mode=pos_mode,
                         text_size=text_size, clip_to_parent=clip_to_parent, self_dimensions=self_dimensions, mode=mode)

        self.pop_offset = pop_offset
        self._hovered = False
        self.original_pos = self.cpos

        self.activation_area = activation_area 

    def adopt(self, parent: QWidget):
        if parent:
            self.setParent(parent)
            self.parent_w = parent.width()
            self.parent_h = parent.height()
            self.load(parent.width(), parent.height())
            parent.setMouseTracking(True)
            parent.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == event.Type.MouseMove and self.activation_area and self.parentWidget() == watched:
            w_area = int(self.activation_area[0] * self.width())
            h_area = int(self.activation_area[1] * self.height())
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
    def __init__(self, bg_color="#FFFFFF", radius=0, border_color=None, border_width=0,
                 pos=(0,0), size=(0,0), stretch=False, pos_mode=cWidget.MOVE_BY_FRACTION, clip_to_parent=True, self_dimensions=0):
        super().__init__(bg_color, radius, border_color, border_width, pos, size, stretch, pos_mode=pos_mode ,clip_to_parent=clip_to_parent, self_dimensions=self_dimensions)
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
    def __init__(self, bg_color="#FFFFFF", radius=0, border_color=None, border_width=0,
                 pos=(0,0), size=(0,0), stretch=False, pos_mode=cWidget.MOVE_BY_FRACTION, clip_to_parent=True, self_dimensions=0):
        super().__init__(bg_color, radius, border_color, border_width, pos, size, stretch, pos_mode=pos_mode ,clip_to_parent=clip_to_parent, self_dimensions=self_dimensions)

    def add_widget(self, widget: cWidget):
        self.widgets.append(widget)
        widget.setParent(self)
        widget.parent_h = self.height()
        widget.parent_w = self.width()
        self.load_widgets()

    def load_widgets(self):
        x_offset = 0
        for i in range(len(self.widgets)):
            self.widgets[i].move(x_offset, 0, cWidget.MOVE_BY_PIXEL)
            x_offset += self.widgets[i].width()
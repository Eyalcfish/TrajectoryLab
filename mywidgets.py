import cwidgets

class WidgetWithThreeDots(cwidgets.ccontainerWidget):
    def __init__(self, three_dots_size=(0.4,0.1), widget=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create the three-dots button
        self.three_dots = cwidgets.cButton(
            parent=None,          # only positional argument is parent
            text=":",             # must be keyword
            pos=(0.8, 0),
            size=three_dots_size,
            stretch=False,
            bg_color="#27ae60",
            text_color="#ffffff",
            hover_color="#2ecc71",
            pressed_color="#27ae60",
            radius=100000,
        )
        self.three_dots.clicked.connect(lambda: print("Three dots button clicked!"))

        # Add widgets to container
        self.add_widget(self.three_dots)
        if widget:
            self.add_widget(widget)
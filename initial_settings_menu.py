from custom_widgets import EventMixin, State, fit_text_to_widget
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QPushButton, QSizePolicy, QWidget, QLineEdit, QLabel
from settings_menu_widgets import SettingWidget, SettingWidgetContainer

class InitialSettingsMenu(EventMixin, QWidget):
    def __init__(self, parent = None, background_color = "#ffffff"):
        super().__init__(parent)
        self.background_color = background_color

        self.cupdate(State.DEFAULT)

    def cupdate(self, state: State):
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        if state == State.DEFAULT:
            self.lower()
            self.load_settings_menu()
        if state == State.RESIZE or state == State.DEFAULT:
            self.resize(self.parent_w,self.parent_h)
            self.setStyleSheet(self._stylesheet())

    def load_settings_menu(self):
        self.target_settings = SettingWidgetContainer(category_name="Target Settings", parent=self, w=0.3, h=0.25, x=0.575, y=0.05, background_color="#1A1A1A")
        self.target_height_setting = SettingWidget(default_value=42, setting_name="Target Height", parent=self.target_settings, background_color="#1A1A1A")
        self.target_radius_setting = SettingWidget(default_value=3.14, setting_name="Target Radius", parent=self.target_settings, background_color="#1A1A1A")
        self.distance_tolerance_setting = SettingWidget(default_value = 3.14, setting_name = "Distance Tolerance", parent=self.target_settings, background_color="#1A1A1A")

        self.robot_speed_settings = SettingWidgetContainer(category_name="Robot Speed Settings", parent=self, w=0.3, h=0.15, x=0.575, y=0.35, background_color="#1A1A1A")
        self.max_robot_speed_setting = SettingWidget(default_value=42, setting_name="Max Robot Speed", parent=self.robot_speed_settings, background_color="#1A1A1A")
        self.robot_speed_delta_setting = SettingWidget(default_value=3.14, setting_name="Robot Speed Delta", parent=self.robot_speed_settings, background_color="#1A1A1A")

        self.angle_settings = SettingWidgetContainer(category_name="Angle Settings", parent=self, w=0.3, h=0.25, x=0.175, y=0.05, background_color="#1A1A1A")
        self.max_angle_setting = SettingWidget(default_value=42, setting_name="Max Angle", parent=self.angle_settings, background_color="#1A1A1A")
        self.min_angle_setting = SettingWidget(default_value=3.14, setting_name="Min Angle", parent=self.angle_settings, background_color="#1A1A1A")
        self.angle_delta_setting = SettingWidget(default_value = 3.14, setting_name = "Angle Delta", parent=self.angle_settings, background_color="#1A1A1A")

        self.distance_settings = SettingWidgetContainer(category_name="Distance Settings", parent=self, w=0.3, h=0.25, x=0.175, y=0.35, background_color="#1A1A1A")
        self.max_distance_setting = SettingWidget(default_value=42, setting_name="Max Distance", parent=self.distance_settings, background_color="#1A1A1A")
        self.min_distance_setting = SettingWidget(default_value=3.14, setting_name="Min Distance", parent=self.distance_settings, background_color="#1A1A1A")
        self.distance_delta_setting = SettingWidget(default_value = 3.14, setting_name = "Distance Delta", parent=self.distance_settings, background_color="#1A1A1A")

        self.speed_settings = SettingWidgetContainer(category_name="Speed Settings", parent=self, w=0.3, h=0.25, x=0.175, y=0.65, background_color="#1A1A1A")
        self.max_speed_setting = SettingWidget(default_value=42, setting_name="Max Speed", parent=self.speed_settings, background_color="#1A1A1A")
        self.min_speed_setting = SettingWidget(default_value=3.14, setting_name="Min Speed", parent=self.speed_settings, background_color="#1A1A1A")
        self.delta_speed_setting = SettingWidget(default_value = 3.14, setting_name = "Speed Delta", parent=self.speed_settings, background_color="#1A1A1A")

        # setting1.lineedit.textChanged.connect(lambda x: print(x))

        self.target_settings.add_setting(self.target_height_setting)
        self.target_settings.add_setting(self.target_radius_setting)
        self.target_settings.add_setting(self.distance_tolerance_setting)

        self.robot_speed_settings.add_setting(self.max_robot_speed_setting)
        self.robot_speed_settings.add_setting(self.robot_speed_delta_setting)

        self.angle_settings.add_setting(self.max_angle_setting)
        self.angle_settings.add_setting(self.min_angle_setting)
        self.angle_settings.add_setting(self.angle_delta_setting)

        self.distance_settings.add_setting(self.max_distance_setting)
        self.distance_settings.add_setting(self.min_distance_setting)
        self.distance_settings.add_setting(self.distance_delta_setting)

        self.speed_settings.add_setting(self.max_speed_setting)
        self.speed_settings.add_setting(self.min_speed_setting)
        self.speed_settings.add_setting(self.delta_speed_setting)

    def _stylesheet(self):
        return f"""
            background-color: {self.background_color};
            """
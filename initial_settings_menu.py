import json
from custom_widgets import EventMixin, State, fit_text_to_widget
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer, QThread, QObject, Signal
from PySide6.QtWidgets import QPushButton, QSizePolicy, QWidget, QLineEdit, QLabel
from settings_menu_widgets import SettingWidget, SettingWidgetContainer, csvGenerateButton
import subprocess
import concurrent.futures

class InitialSettingsMenu(EventMixin, QWidget):
    def __init__(self, parent = None, background_color = "#FFFFFF"):
        super().__init__(parent)
        self.background_color = background_color
        self.settings = {}

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        self.cupdate(State.DEFAULT)

    class Worker(QObject):
        finished = Signal()
        output = Signal(str)

        def __init__(self, settings_dict, settings_path, exe_path):
            super().__init__()
            self.settings_dict = settings_dict  # store the Python dict
            self.settings_path = settings_path
            self.exe_path = exe_path

        def run(self):
            # Save JSON first
            with open(self.settings_path, "w") as f:
                json.dump(self.settings_dict, f)

            # Run exe and read stdout live
            process = subprocess.Popen(
                [self.exe_path, self.settings_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                self.output.emit(line.strip())  # send to GUI
            self.finished.emit()

    def cupdate(self, state: State):
        self.parent_w = self.parent().width()
        self.parent_h = self.parent().height()
        if state == State.DEFAULT:
            self.lower()
            self.load_settings_menu()
        if state == State.RESIZE or state == State.DEFAULT:
            self.resize(self.parent_w,self.parent_h)
            self.setStyleSheet(self._stylesheet())

    def change_setting(self, setting, value):
        if value == "":
            del self.settings[setting]
        else:
            self.settings[setting] = float(value)

    def generate_json(self):
        self.csv_button.setEnabled(False)
        self.thread = QThread()
        self.worker = self.Worker(self.settings ,"settings/data.json", "/home/eyalc/Projects/TrajectoryLab/TrajectoryLab/shootingsim.exe")
        self.worker.moveToThread(self.thread)

        def set_button_prec(prec):
            self.csv_button.prec = float(prec)/100
            self.csv_button.cupdate(State.REPAINT)

        def finish_worker():
            self.csv_button.prec = 0
            self.csv_button.cupdate(State.REPAINT)
            self.csv_button.setEnabled(True)
            
        self.thread.started.connect(self.worker.run)
        self.worker.output.connect(lambda prec: set_button_prec(prec))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(lambda: finish_worker())
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        


    def load_settings_menu(self):
        self.target_settings = SettingWidgetContainer(category_name="Target Settings", parent=self, w=0.3, h=0.25, x=0.175, y=0.65, background_color="#0D0D0D")
        self.target_height_setting = SettingWidget(default_value=42, setting_name="Target Height", parent=self.target_settings, background_color="#0D0D0D")
        self.target_radius_setting = SettingWidget(default_value=3.14, setting_name="Target Radius", parent=self.target_settings, background_color="#0D0D0D")
        self.distance_tolerance_setting = SettingWidget(default_value = 3.14, setting_name = "Distance Tolerance", parent=self.target_settings, background_color="#0D0D0D")

        self.robot_speed_settings = SettingWidgetContainer(category_name="Robot Speed Settings", parent=self, w=0.3, h=0.15, x=0.575, y=0.35, background_color="#0D0D0D")
        self.max_robot_speed_setting = SettingWidget(default_value=42, setting_name="Max Robot Speed", parent=self.robot_speed_settings, background_color="#0D0D0D")
        self.robot_speed_delta_setting = SettingWidget(default_value=3.14, setting_name="Robot Speed Delta", parent=self.robot_speed_settings, background_color="#0D0D0D")

        self.angle_settings = SettingWidgetContainer(category_name="Angle Settings", parent=self, w=0.3, h=0.25, x=0.175, y=0.05, background_color="#0D0D0D")
        self.max_angle_setting = SettingWidget(default_value=42, setting_name="Max Angle", parent=self.angle_settings, background_color="#0D0D0D")
        self.min_angle_setting = SettingWidget(default_value=3.14, setting_name="Min Angle", parent=self.angle_settings, background_color="#0D0D0D")
        self.angle_delta_setting = SettingWidget(default_value = 3.14, setting_name = "Angle Delta", parent=self.angle_settings, background_color="#0D0D0D")

        self.distance_settings = SettingWidgetContainer(category_name="Distance Settings", parent=self, w=0.3, h=0.25, x=0.575, y=0.05, background_color="#0D0D0D")
        self.max_distance_setting = SettingWidget(default_value=42, setting_name="Max Distance", parent=self.distance_settings, background_color="#0D0D0D")
        self.min_distance_setting = SettingWidget(default_value=3.14, setting_name="Min Distance", parent=self.distance_settings, background_color="#0D0D0D")
        self.distance_delta_setting = SettingWidget(default_value = 3.14, setting_name = "Distance Delta", parent=self.distance_settings, background_color="#0D0D0D")

        self.speed_settings = SettingWidgetContainer(category_name="Shooter Speed Settings", parent=self, w=0.3, h=0.25, x=0.175, y=0.35, background_color="#0D0D0D")
        self.max_speed_setting = SettingWidget(default_value=42, setting_name="Max Shooter Speed", parent=self.speed_settings, background_color="#0D0D0D")
        self.min_speed_setting = SettingWidget(default_value=3.14, setting_name="Min Shooter Speed", parent=self.speed_settings, background_color="#0D0D0D")
        self.delta_speed_setting = SettingWidget(default_value = 3.14, setting_name = "Shooter Speed Delta", parent=self.speed_settings, background_color="#0D0D0D")

        self.target_height_setting.lineedit.textChanged.connect(lambda x: self.change_setting("target_height", x))
        self.target_radius_setting.lineedit.textChanged.connect(lambda x: self.change_setting("target_radius", x))
        self.distance_tolerance_setting.lineedit.textChanged.connect(lambda x: self.change_setting("distance_tolerance", x))

        self.max_robot_speed_setting.lineedit.textChanged.connect(lambda x: self.change_setting("max_robot_speed", x))
        self.robot_speed_delta_setting.lineedit.textChanged.connect(lambda x: self.change_setting("robot_speed_delta", x))

        self.max_angle_setting.lineedit.textChanged.connect(lambda x: self.change_setting("max_angle", x))
        self.min_angle_setting.lineedit.textChanged.connect(lambda x: self.change_setting("min_angle", x))
        self.angle_delta_setting.lineedit.textChanged.connect(lambda x: self.change_setting("angle_delta", x))

        self.max_distance_setting.lineedit.textChanged.connect(lambda x: self.change_setting("max_distance", x))
        self.min_distance_setting.lineedit.textChanged.connect(lambda x: self.change_setting("min_distance", x))
        self.distance_delta_setting.lineedit.textChanged.connect(lambda x: self.change_setting("distance_delta", x))

        self.max_speed_setting.lineedit.textChanged.connect(lambda x: self.change_setting("max_speed", x))
        self.min_speed_setting.lineedit.textChanged.connect(lambda x: self.change_setting("min_speed", x))
        self.delta_speed_setting.lineedit.textChanged.connect(lambda x: self.change_setting("delta_speed", x))

        self.csv_button = csvGenerateButton(text="Generate CSV", parent=self, w=0.3, h=0.25, x_pos=0.575, y_pos=0.65)

        self.csv_button.clicked.connect(self.generate_json)

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
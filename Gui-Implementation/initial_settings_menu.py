import json
import os
from custom_widgets import EventMixin, State, fit_text_to_widget
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer, QThread, QObject, Signal
from PySide6.QtWidgets import QPushButton, QSizePolicy, QWidget, QLineEdit, QLabel
from settings_menu_widgets import SettingWidget, SettingWidgetContainer, csvGenerateButton
import subprocess
import concurrent.futures
import filemanagment as filemanagment
from pathlib import Path
import color_palette as cp

class InitialSettingsMenu(EventMixin, QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.settings = {}

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        self.cupdate(State.DEFAULT)

    class Worker(QObject):
        finished = Signal()
        output = Signal(str)

        def __init__(self, settings_dict, generation_id, exe_path):
            super().__init__()
            self.settings_dict = settings_dict 
            self.exe_path = exe_path
            self.generation_id = generation_id

        def run(self):
            folder = Path(f"profiles/profile_{self.generation_id}")
            folder.mkdir(parents=True, exist_ok=True)

            with open(folder / "settings.json", "w") as f:
                json.dump(self.settings_dict, f)

            settings_path = str(folder.joinpath("settings.json").absolute())
            output_path = str(folder.joinpath("output.csv").absolute())
            
            exe_path = str(Path(__file__).parent.absolute() / self.exe_path)

            try:
                process = subprocess.Popen(
                    [exe_path, settings_path, output_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )

                for line in process.stdout:
                    self.output.emit(line.strip())

                process.wait()

                if process.returncode != 0:
                    stderr_output = process.stderr.read()
                    print("Error executing the simulation:")
                    print(f"Return Code: {process.returncode}")
                    print("STDERR:")
                    print(stderr_output)
                else:
                    print("Simulation executed successfully.")

            except FileNotFoundError:
                print(f"Error: The executable at {exe_path} was not found.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

            self.finished.emit()

    def generate_json(self, generation_id):
        self.csv_button.setEnabled(False)
        self.thread = QThread()
        self.worker = self.Worker(settings_dict=self.settings , generation_id= generation_id, exe_path="shootingsim.exe")
        self.worker.moveToThread(self.thread)

        def set_button_prec(prec: str):
            prec = prec.replace(" %","")
            try:
                self.csv_button.prec = float(prec)/100
                self.csv_button.cupdate(State.REPAINT)
            except:
                pass

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

        


    def load_settings_menu(self):
        self.target_settings = SettingWidgetContainer(category_name="Target Settings", parent=self, w=0.3, h=0.25, x=0.175, y=0.65)
        self.target_height_setting = SettingWidget(default_value=42, setting_name="Target Height", parent=self.target_settings)
        self.target_radius_setting = SettingWidget(default_value=3.14, setting_name="Target Radius", parent=self.target_settings)
        self.distance_tolerance_setting = SettingWidget(default_value = 3.14, setting_name = "Distance Tolerance", parent=self.target_settings)

        self.robot_speed_settings = SettingWidgetContainer(category_name="Robot Speed Settings", parent=self, w=0.3, h=0.15, x=0.575, y=0.35)
        self.max_robot_speed_setting = SettingWidget(default_value=42, setting_name="Max Robot Speed", parent=self.robot_speed_settings)
        self.robot_speed_delta_setting = SettingWidget(default_value=3.14, setting_name="Robot Speed Delta", parent=self.robot_speed_settings)

        self.angle_settings = SettingWidgetContainer(category_name="Angle Settings", parent=self, w=0.3, h=0.25, x=0.175, y=0.05)
        self.max_angle_setting = SettingWidget(default_value=42, setting_name="Max Angle", parent=self.angle_settings)
        self.min_angle_setting = SettingWidget(default_value=3.14, setting_name="Min Angle", parent=self.angle_settings)
        self.angle_delta_setting = SettingWidget(default_value = 3.14, setting_name = "Angle Delta", parent=self.angle_settings)

        self.distance_settings = SettingWidgetContainer(category_name="Distance Settings", parent=self, w=0.3, h=0.25, x=0.575, y=0.05)
        self.max_distance_setting = SettingWidget(default_value=42, setting_name="Max Distance", parent=self.distance_settings)
        self.min_distance_setting = SettingWidget(default_value=3.14, setting_name="Min Distance", parent=self.distance_settings)
        self.distance_delta_setting = SettingWidget(default_value = 3.14, setting_name = "Distance Delta", parent=self.distance_settings)

        self.speed_settings = SettingWidgetContainer(category_name="Shooter Speed Settings", parent=self, w=0.3, h=0.25, x=0.175, y=0.35)
        self.max_speed_setting = SettingWidget(default_value=42, setting_name="Max Shooter Speed", parent=self.speed_settings)
        self.min_speed_setting = SettingWidget(default_value=3.14, setting_name="Min Shooter Speed", parent=self.speed_settings)
        self.delta_speed_setting = SettingWidget(default_value = 3.14, setting_name = "Shooter Speed Delta", parent=self.speed_settings)

        self.target_height_setting.lineedit.textChanged.connect(lambda x: self.change_setting("targetheight", x))
        self.target_radius_setting.lineedit.textChanged.connect(lambda x: self.change_setting("targetradius", x))
        self.distance_tolerance_setting.lineedit.textChanged.connect(lambda x: self.change_setting("distancetolerance", x))

        self.max_robot_speed_setting.lineedit.textChanged.connect(lambda x: self.change_setting("maxrobotspeed", x))
        self.robot_speed_delta_setting.lineedit.textChanged.connect(lambda x: self.change_setting("deltarobotspeed", x))

        self.max_angle_setting.lineedit.textChanged.connect(lambda x: self.change_setting("maxangle", x))
        self.min_angle_setting.lineedit.textChanged.connect(lambda x: self.change_setting("minangle", x))
        self.angle_delta_setting.lineedit.textChanged.connect(lambda x: self.change_setting("deltaangle", x))

        self.max_distance_setting.lineedit.textChanged.connect(lambda x: self.change_setting("maxdistance", x))
        self.min_distance_setting.lineedit.textChanged.connect(lambda x: self.change_setting("mindistance", x))
        self.distance_delta_setting.lineedit.textChanged.connect(lambda x: self.change_setting("deltadistance", x))

        self.max_speed_setting.lineedit.textChanged.connect(lambda x: self.change_setting("maxspeed", x))
        self.min_speed_setting.lineedit.textChanged.connect(lambda x: self.change_setting("minspeed", x))
        self.delta_speed_setting.lineedit.textChanged.connect(lambda x: self.change_setting("deltaspeed", x))

        self.csv_button = csvGenerateButton(text="Generate CSV", parent=self, w=0.3, h=0.25, x_pos=0.575, y_pos=0.65)

        self.csv_button.clicked.connect(lambda: self.generate_json(filemanagment.get_latest_id()+1))

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
            background-color: {cp.TRANSPARENT};
            """
    

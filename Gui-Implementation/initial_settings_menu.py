import json
import subprocess
from pathlib import Path
from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import QThread, QObject, Signal
from settings_menu_widgets import SettingWidget, SettingWidgetContainer, CSVGenerateButton
import filemanagment
import color_palette as cp

class SimulationWorker(QObject):
    """Worker thread for running the shooting simulation."""
    finished = Signal()
    output = Signal(str)

    def __init__(self, settings, generation_id, exe_path):
        super().__init__()
        self.settings = settings
        self.generation_id = generation_id
        self.exe_path = exe_path

    def run(self):
        """Execute the simulation subprocess."""
        profile_dir = Path(f"profiles/profile_{self.generation_id}")
        profile_dir.mkdir(parents=True, exist_ok=True)

        settings_path = profile_dir / "settings.json"
        with open(settings_path, "w") as f:
            json.dump(self.settings, f)

        output_path = profile_dir / "output.csv"
        exe_abs_path = Path(__file__).parent.absolute() / self.exe_path

        try:
            process = subprocess.Popen(
                [str(exe_abs_path), str(settings_path.absolute()), str(output_path.absolute())],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True
            )
            for line in iter(process.stdout.readline, ''):
                self.output.emit(line.strip())
            process.stdout.close()
            process.wait()

            if process.returncode != 0:
                print(f"Error in simulation: {process.stderr.read()}")

        except FileNotFoundError:
            print(f"Error: Executable not found at {exe_abs_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            self.finished.emit()

from PySide6.QtWidgets import QWidget, QGridLayout

class InitialSettingsMenu(QWidget):
    """Menu for configuring and launching the initial simulation settings."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = {}
        self.setStyleSheet(f"background-color: {cp.TRANSPARENT};")
        
        # Main layout
        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)

        self._load_settings_widgets(layout)

    def _load_settings_widgets(self, layout: QGridLayout):
        """Load and connect all the setting widgets."""
        self._create_setting_groups(layout)
        self._connect_signals()

    def _create_setting_groups(self, layout: QGridLayout):
        """Create all the setting widget containers and their children."""
        setting_definitions = {
            "Angle Settings": ([("Max Angle", 42), ("Min Angle", 3.14), ("Angle Delta", 3.14)], 0, 0),
            "Shooter Speed Settings": ([("Max Shooter Speed", 42), ("Min Shooter Speed", 3.14), ("Shooter Speed Delta", 3.14)], 1, 0),
            "Target Settings": ([("Target Height", 42), ("Target Radius", 3.14), ("Distance Tolerance", 3.14)], 2, 0),
            "Distance Settings": ([("Max Distance", 42), ("Min Distance", 3.14), ("Distance Delta", 3.14)], 0, 1),
            "Robot Speed Settings": ([("Max Robot Speed", 42), ("Min Robot Speed", 3.14), ("Shooter Speed Delta", 3.14)], 1, 1),
        }

        for category, (settings, row, col) in setting_definitions.items():
            container = SettingWidgetContainer(category, self)
            for name, val in settings:
                setting_widget = SettingWidget(val, name, container)
                container.add_setting(setting_widget)
                setting_widget.lineedit.textChanged.connect(
                    lambda text, name=name: self._change_setting(name.lower().replace(" ", ""), text)
                )
            layout.addWidget(container, row, col)
        
        self.csv_button = CSVGenerateButton("Generate CSV", self)
        layout.addWidget(self.csv_button, 2, 1)

    def _connect_signals(self):
        """Connect widget signals to their respective slots."""
        self.csv_button.clicked.connect(self._run_simulation)

    def _change_setting(self, setting, value):
        """Update a setting value."""
        if value:
            try:
                self.settings[setting] = float(value)
            except ValueError:
                # Handle cases where the text is not a valid float, e.g., just a "-"
                if setting in self.settings:
                    del self.settings[setting]
        elif setting in self.settings:
            del self.settings[setting]

    def _run_simulation(self):
        """Run the simulation in a separate thread."""
        self.csv_button.setEnabled(False)
        generation_id = filemanagment.get_latest_id() + 1
        
        thread = QThread() # Make thread a local variable
        worker = SimulationWorker(self.settings, generation_id, "shootingsim.exe") # Make worker a local variable
        worker.moveToThread(thread)

        worker.output.connect(self._update_progress)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater) # Worker deletes itself
        thread.finished.connect(thread.deleteLater) # Thread deletes itself
        worker.finished.connect(self._on_simulation_finish)
        
        thread.start()

    def _update_progress(self, text):
        """Update the progress bar on the CSV button."""
        try:
            progress_value = float(text.replace(" %", ""))
            self.csv_button.set_progress(progress_value)
        except (ValueError, AttributeError):
            # Ignore lines that aren't progress updates
            pass

    def _on_simulation_finish(self):
        """Reset the CSV button after the simulation finishes."""
        self.csv_button.set_progress(0)
        self.csv_button.setEnabled(True)
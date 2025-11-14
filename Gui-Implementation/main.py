import sys
import shutil
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import QRect, Qt, QThread, QObject, Signal
from vscode_style_widgets import VSCodeSidebar, TabBar, Workspace
from tab_content_viewers import SettingsFileViewer, CSVFileViewer, PlaceholderViewer
import color_palette as cp
from pathlib import Path

class SimulationWorker(QObject):
    """Worker thread for running the simulation."""
    progress_updated = Signal(int)
    simulation_finished = Signal(str)

    def __init__(self, settings_path):
        super().__init__()
        self.settings_path = settings_path

    def run(self):
        """Run the simulation."""
        settings_path = Path(self.settings_path)
        profile_dir = settings_path.parent
        output_csv_path = profile_dir / 'output.csv'

        try:
            process = subprocess.Popen(['shootingsim.exe', str(settings_path), str(output_csv_path)],
                                       stdin=subprocess.DEVNULL,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW, bufsize=1, universal_newlines=True)

            for line in iter(process.stdout.readline, ''):
                try:
                    progress = int(float(line.strip().replace('%', '')))
                    self.progress_updated.emit(progress)
                except ValueError:
                    pass
            
            process.stdout.close()
            return_code = process.wait()

            if return_code != 0:
                print(f"Error running simulation: return code {return_code}")
                self.simulation_finished.emit("")
            else:
                self.simulation_finished.emit(str(output_csv_path))

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error running simulation: {e}")
            self.simulation_finished.emit("")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.simulation_finished.emit("")


class MainWindow(QWidget):
    """Main window for the Trajectory Lab application with VS Code-style interface."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trajectory Lab")
        self.setStyleSheet(f"background-color: {cp.BACKGROUND_STYLES['main_window']['color']};")
        self.resize(1200, 700)

        # Track open tabs and their content
        self.tab_content_map = {}  # Maps tab index to workspace content index

        # Main horizontal layout: sidebar + content area
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left sidebar
        self.sidebar = VSCodeSidebar(self)
        self.sidebar.settings_clicked.connect(self._open_settings_file)
        self.sidebar.csv_clicked.connect(self._open_csv_file)
        
        main_layout.addWidget(self.sidebar)

        # Right content area: tab bar + workspace
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Tab bar
        self.tab_bar = TabBar(self)
        self.tab_bar.tab_selected.connect(self._on_tab_selected)
        self.tab_bar.tab_closed.connect(self._on_tab_closed)
        
        content_layout.addWidget(self.tab_bar)

        # Workspace
        self.workspace = Workspace(self)
        content_layout.addWidget(self.workspace)

        content_layout.setStretch(1, 1)
        main_layout.addWidget(content_area)
        main_layout.setStretch(1, 1)

        self.setLayout(main_layout)
        self.thread = None

    def closeEvent(self, event):
        """Handle the window close event."""
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        event.accept()

    def _open_settings_file(self):
        """Open the base_settings.json file in a new tab."""
        file_path = "base_settings.json"
        tab_title = "New Profile"

        for i in range(len(self.tab_bar.tabs)):
            if self.tab_bar.get_tab_title(i) == tab_title:
                self.tab_bar.select_tab(i)
                return

        settings_viewer = SettingsFileViewer()
        settings_viewer.load_settings_file(file_path)
        settings_viewer.profile_saved.connect(self._on_profile_saved)

        content_index = self.workspace.add_content(settings_viewer)
        tab_index = self.tab_bar.add_tab(tab_title)
        self.tab_content_map[tab_index] = content_index
        self.tab_bar.select_tab(tab_index)

    def _on_profile_saved(self, settings_path):
        """Handle the profile_saved signal."""
        current_tab_index = self.tab_bar.current_tab
        content_index = self.tab_content_map[current_tab_index]
        settings_viewer = self.workspace.stacked_widget.widget(content_index)

        # Create and start the simulation worker
        self.thread = QThread()
        self.worker = SimulationWorker(settings_path)
        self.worker.moveToThread(self.thread)

        self.worker.progress_updated.connect(settings_viewer.update_progress)
        self.worker.simulation_finished.connect(self._simulation_finished)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def _update_progress(self, value):
        """Update the progress label."""
        # This method is no longer needed here, as the progress is updated directly in the SettingsFileViewer
        pass

    def _simulation_finished(self, csv_path):
        """Handle the simulation_finished signal."""
        self.thread.quit()
        self.thread.wait()

        # Re-enable the save button and clear the progress label
        current_tab_index = self.tab_bar.current_tab
        content_index = self.tab_content_map[current_tab_index]
        settings_viewer = self.workspace.stacked_widget.widget(content_index)
        if isinstance(settings_viewer, SettingsFileViewer):
            settings_viewer.simulation_finished()

        if csv_path:
            path = Path(csv_path)
            if path.exists():
                profile_num = int(path.parent.name.split('_')[-1])
                self._open_csv_file(profile_num)
                self.sidebar.reload_csv_section()


    def _open_csv_file(self, csv_num):
        """Open the output.csv file for the specified profile_num."""
        file_path = Path(f"profiles/profile_{csv_num}/output.csv")
        tab_title = f"Profile {csv_num}"

        # Check if a tab for this CSV is already open
        for i in range(len(self.tab_bar.tabs)):
            if self.tab_bar.get_tab_title(i) == tab_title:
                self.tab_bar.select_tab(i)
                return

        if not file_path.exists():
            print(f"Error: File not found at {file_path}")
            return

        csv_viewer = CSVFileViewer(self)
        csv_viewer.load_csv_file(str(file_path), title=tab_title)
        csv_viewer.profile_deleted.connect(self._on_profile_deleted)

        # Add a new tab for the CSV viewer
        content_index = self.workspace.add_content(csv_viewer)
        tab_index = self.tab_bar.add_tab(tab_title)
        self.tab_content_map[tab_index] = content_index
        self.tab_bar.select_tab(tab_index)

    def _on_profile_deleted(self, file_path):
        """Handle the profile_deleted signal."""
        profile_dir = Path(file_path).parent
        shutil.rmtree(profile_dir)
        self.tab_bar.close_tab(self.tab_bar.current_tab)
        self.sidebar.reload_csv_section()

    def _on_tab_selected(self, tab_index):
        """Handle tab selection - show corresponding content."""
        if tab_index in self.tab_content_map:
            content_index = self.tab_content_map[tab_index]
            self.workspace.show_content(content_index)
        else:
            self.workspace.show_empty()

    def _on_tab_closed(self, tab_index):
        """Handle tab closure - remove content and update mapping."""
        if tab_index in self.tab_content_map:
            content_index = self.tab_content_map[tab_index]
            self.workspace.remove_content(content_index)
            del self.tab_content_map[tab_index]

            new_map = {}
            for idx, content_idx in self.tab_content_map.items():
                if idx > tab_index:
                    new_map[idx - 1] = content_idx
                else:
                    new_map[idx] = content_idx
            self.tab_content_map = new_map

        if not self.tab_bar.tabs:
            self.workspace.show_empty()


class App:
    """Main application class."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

    def run(self):
        """Show the main window and run the application."""
        self.window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    import threading
    app = App()
    app.run()

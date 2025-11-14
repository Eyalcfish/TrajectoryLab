from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QScrollArea, QFrame, QStackedWidget)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
import color_palette as cp
from pathlib import Path

class VSCodeSidebar(QWidget):
    """VS Code-style sidebar with logo, settings button, and collapsible CSV section."""

    settings_clicked = Signal()
    csv_clicked = Signal(int)  # Emits CSV number (1, 2, or 3)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(220)  # VS Code-style narrow sidebar
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {cp.BACKGROUND_STYLES['sidebar']['color']};
                color: {cp.PRIMARY_TEXT};
                border-right: 1px solid {cp.BORDER_DIVIDER};
            }}
        """
)
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo section at top
        self.logo_container = self._create_logo_section()
        layout.addWidget(self.logo_container)

        # Settings button
        self.settings_button = self._create_settings_button()
        layout.addWidget(self.settings_button)

        # CSV section (collapsible)
        self.csv_section = self._create_csv_section()
        layout.addWidget(self.csv_section)

        # Spacer to push everything to top
        layout.addStretch()

        self.setLayout(layout)

    def _create_logo_section(self):
        """Create the logo container at the top."""
        container = QWidget()
        container.setFixedHeight(80)
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {cp.BACKGROUND_STYLES['sidebar']['color']};
                border-bottom: 1px solid {cp.BORDER_DIVIDER};
            }}
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setAlignment(Qt.AlignCenter)

        # Compact, elegant logo
        logo_label = QLabel("TrajectoryLab")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                font-weight: 600;
                color: {cp.PRIMARY_BLUE};
                background-color: {cp.CARD_SURFACE};
                border-radius: 6px;
                padding: 12px 16px;
                border: 1px solid {cp.BORDER_DIVIDER};
            }}
        """)

        layout.addWidget(logo_label)
        return container

    def _create_settings_button(self):
        """Create the Settings File button."""
        button = QPushButton("⚙ settings.json")
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {cp.CARD_SURFACE};
                color: {cp.SECONDARY_TEXT};
                text-align: left;
                padding: 6px 16px;
                border: none;
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border-right: 1px solid {cp.BORDER_DIVIDER}; 
            }}
            QPushButton:hover {{
                color: {cp.PRIMARY_TEXT};
                background-color: {cp.BORDER_DIVIDER};
            }}
            QPushButton:checked {{
                color: {cp.PRIMARY_TEXT};
                background-color: {cp.BORDER_DIVIDER};
            }}
        """)
        button.clicked.connect(self.settings_clicked.emit)
        return button

    def _create_csv_section(self):
        """Create the collapsible CSV section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # CSV header (collapsible toggle)
        self.csv_header = QPushButton("▼ CSVs")
        self.csv_header.setCursor(Qt.PointingHandCursor)
        self.csv_header.setCheckable(True)
        self.csv_header.setChecked(True)  # Start expanded
        self.csv_header.setStyleSheet(f"""
            QPushButton {{
                background-color: {cp.CARD_SURFACE};
                color: {cp.SECONDARY_TEXT};
                text-align: left;
                padding: 6px 16px;
                border: none;
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border: 1px solid {cp.BORDER_DIVIDER};
            }}
            QPushButton:hover {{
                color: {cp.PRIMARY_TEXT};
            }}
            QPushButton:checked {{
                color: {cp.PRIMARY_TEXT};
            }}
        """)
        self.csv_header.toggled.connect(self._toggle_csv_content)
        layout.addWidget(self.csv_header)

        # CSV content (the 3 CSV buttons)
        self.csv_content = QWidget()
        csv_content_layout = QVBoxLayout(self.csv_content)
        csv_content_layout.setContentsMargins(0, 0, 0, 0)
        csv_content_layout.setSpacing(0)

        # --- 1. Find all matching CSV files ---
        profile_dir = Path('profiles')
        # We use list() to get all paths, so we can sort them
        csv_paths = list(profile_dir.glob('profile_*/output.csv'))

        # --- 2. Sort the paths numerically ---
        # (This prevents 'profile_10' from coming before 'profile_2')
        def get_profile_num(path):
            try:
                # Gets 'profile_1' -> '1' -> 1
                return int(path.parent.name.split('_')[-1])
            except (ValueError, IndexError):
                return -1 # In case of a badly named folder

        csv_paths.sort(key=get_profile_num)
        
        # --- 3. Create a button for each CSV ---
        for csv_path in csv_paths:
            try:
                # Get the profile number (e.g., 1, 2, 3...)
                profile_num = get_profile_num(csv_path)
                if profile_num == -1:
                    continue # Skip invalid folders

                button_title = f"Profile {profile_num}"

                button = QPushButton(button_title)
                button.setCursor(Qt.PointingHandCursor)
                button.setStyleSheet(f"""
                    QPushButton {{
                        color: {cp.SECONDARY_TEXT};
                        background-color: transparent;
                        border: none;
                        padding: 6px 0px 6px 20px; /* Indented padding */
                        text-align: left;
                        font-size: 13px;
                        border-right: 1px solid {cp.BORDER_DIVIDER};
                        border-left: 1px solid {cp.BORDER_DIVIDER};
                        border-bottom: 1px solid {cp.BORDER_DIVIDER};
                    }}
                    QPushButton:hover {{
                        background-color: rgba(255, 255, 255, 0.05);
                        color: {cp.PRIMARY_TEXT};
                    }}
                """)

                button.clicked.connect(lambda checked, num=profile_num: self.csv_clicked.emit(num))
                
                csv_content_layout.addWidget(button)

            except Exception as e:
                print(f"Error processing {csv_path}: {e}")
                continue

        layout.addWidget(self.csv_content)
        return container

    def _create_csv_button(self, text, csv_num):
        """Create a single CSV button."""
        button = QPushButton(f"📄 {text}")
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {cp.CARD_SURFACE};
                color: {cp.SECONDARY_TEXT};
                text-align: left;
                padding: 6px 16px 6px 32px;
                border: none;
                font-size: 12px;
                font-family: "Segoe UI", "Roboto", sans-serif;
                border-right: 1px solid {cp.BORDER_DIVIDER};
                border-bottom: 1px solid {cp.BORDER_DIVIDER};
            }}
            QPushButton:hover {{
                background-color: {cp.BORDER_DIVIDER}; /* Use a color from the palette */
                color: {cp.PRIMARY_TEXT};
            }}
            QPushButton:pressed {{
                background-color: {cp.BACKGROUND_DARK}; /* Use a color from the palette */
            }}
        """)
        button.clicked.connect(lambda: self.csv_clicked.emit(csv_num))
        return button

    def reload_csv_section(self):
        """Reload the CSV section to show new profiles."""
        # Clear existing buttons
        for i in reversed(range(self.csv_content.layout().count())):
            self.csv_content.layout().itemAt(i).widget().setParent(None)

        # --- 1. Find all matching CSV files ---
        profile_dir = Path('profiles')
        csv_paths = list(profile_dir.glob('profile_*/output.csv'))

        # --- 2. Sort the paths numerically ---
        def get_profile_num(path):
            try:
                return int(path.parent.name.split('_')[-1])
            except (ValueError, IndexError):
                return -1

        csv_paths.sort(key=get_profile_num)
        
        # --- 3. Create a button for each CSV ---
        for csv_path in csv_paths:
            try:
                profile_num = get_profile_num(csv_path)
                if profile_num == -1:
                    continue

                button_title = f"Profile {profile_num}"

                button = QPushButton(button_title)
                button.setCursor(Qt.PointingHandCursor)
                button.setStyleSheet(f"""
                    QPushButton {{
                        color: {cp.SECONDARY_TEXT};
                        background-color: transparent;
                        border: none;
                        padding: 6px 0px 6px 20px; /* Indented padding */
                        text-align: left;
                        font-size: 13px;
                        border-right: 1px solid {cp.BORDER_DIVIDER};
                        border-left: 1px solid {cp.BORDER_DIVIDER};
                        border-bottom: 1px solid {cp.BORDER_DIVIDER};
                    }}
                    QPushButton:hover {{
                        background-color: rgba(255, 255, 255, 0.05);
                        color: {cp.PRIMARY_TEXT};
                    }}
                """)

                button.clicked.connect(lambda checked, num=profile_num: self.csv_clicked.emit(num))
                
                self.csv_content.layout().addWidget(button)

            except Exception as e:
                print(f"Error processing {csv_path}: {e}")
                continue

    def _toggle_csv_content(self, checked):
        """Toggle the visibility of CSV buttons."""
        self.csv_content.setVisible(checked)
        # Update arrow direction
        if checked:
            self.csv_header.setText("▼ CSVs")
        else:
            self.csv_header.setText("▶ CSVs")


class TabBar(QWidget):
    """VS Code-style tab bar for managing open files."""

    tab_selected = Signal(int)  # Emits tab index
    tab_closed = Signal(int)    # Emits tab index

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(26)  # VS Code tab bar height
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {cp.BACKGROUND_DARK};
                border-bottom: 1px solid {cp.BORDER_DIVIDER};
            }}
        """)

        # Horizontal layout for tabs
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignLeft)

        self.tabs = []
        self.current_tab = -1

    def add_tab(self, title):
        """Add a new tab with the given title."""
        tab = Tab(title, len(self.tabs))
        tab.selected.connect(self._on_tab_selected)
        tab.close_requested.connect(self._on_tab_close_requested)

        self.layout.addWidget(tab)
        self.tabs.append(tab)

        # Select the new tab
        self.select_tab(len(self.tabs) - 1)
        return len(self.tabs) - 1

    def select_tab(self, index):
        """Select a tab by index."""
        if 0 <= index < len(self.tabs):
            # Deselect all tabs
            for tab in self.tabs:
                tab.set_active(False)

            # Select the target tab
            self.tabs[index].set_active(True)
            self.current_tab = index
            self.tab_selected.emit(index)

    def close_tab(self, index):
        """Close a tab by index."""
        if 0 <= index < len(self.tabs):
            tab = self.tabs.pop(index)
            tab.deleteLater()

            # Update indices for remaining tabs
            for i, t in enumerate(self.tabs):
                t.index = i

            # If we closed the current tab, select another
            if index == self.current_tab:
                if self.tabs:
                    # Select the previous tab, or the first one
                    new_index = max(0, index - 1)
                    self.select_tab(new_index)
                else:
                    self.current_tab = -1
            elif index < self.current_tab:
                self.current_tab -= 1

            self.tab_closed.emit(index)

    def _on_tab_selected(self, index):
        """Handle tab selection."""
        self.select_tab(index)

    def _on_tab_close_requested(self, index):
        """Handle tab close request."""
        self.close_tab(index)

    def get_tab_title(self, index):
        """Get the title of a tab by index."""
        if 0 <= index < len(self.tabs):
            return self.tabs[index].title
        return None


class Tab(QWidget):
    """Individual tab in the tab bar."""

    selected = Signal(int)       # Emits tab index
    close_requested = Signal(int) # Emits tab index

    def __init__(self, title, index, parent=None):
        super().__init__(parent)
        self.title = title
        self.index = index
        self.is_active = False

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(26)
        self.setMinimumWidth(100)
        self.setMaximumWidth(180)

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)
        # Title label
        self.title_label = QLabel(title)
        layout.addWidget(self.title_label)

        # Close button
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(18, 18)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {cp.SECONDARY_TEXT};
                border: none;
                border-radius: 2px;
                font-size: 18px;
                font-weight: 300;
                padding: 0;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                color: {cp.PRIMARY_TEXT};
            }}
        """)
        self.close_button.clicked.connect(lambda: self.close_requested.emit(self.index))
        layout.addWidget(self.close_button)

        self._update_style()

    def set_active(self, active):
        """Set the active state of the tab."""
        self.is_active = active
        self._update_style()

    def _update_style(self):
        """Update the tab's visual style based on active state."""
        if self.is_active:
            # --- ACTIVE STYLE ---
            self.setStyleSheet(f"""
                Tab {{
                    background-color: {cp.BACKGROUND_DARK};
                    border: none; /* Remove all other borders */
                    border: 2px solid {cp.PRIMARY_BLUE}; /* Set ONLY the bottom border */
                }}
            """)
            self.title_label.setStyleSheet(f"""
                background-color: transparent;
                color: {cp.PRIMARY_TEXT};
                font-size: 12px;
                font-family: "Segoe UI", "Roboto", sans-serif;
                border: none; /* Add this to prevent border from main style */
            """)
        else:
            # --- INACTIVE STYLE ---
            self.setStyleSheet(f"""
                Tab {{
                    background-color: {cp.CARD_SURFACE};
                    border: 1px solid {cp.BORDER_DIVIDER}; 
                    
                    /* This is the key: make the bottom border 2px
                       but transparent so it holds the space */
                }}
                Tab:hover {{
                    background-color: {cp.BORDER_DIVIDER};
                    border: 1px solid {cp.BORDER_DIVIDER};
                    border-bottom: 2px solid {cp.PRIMARY_BLUE}; /* Show blue underline on hover */
                }}
            """)
            self.title_label.setStyleSheet(f"""
                background-color: transparent;
                color: {cp.SECONDARY_TEXT};
                font-size: 12px;
                font-family: "Segoe UI", "Roboto", sans-serif;
                border: none; /* Add this to prevent border from main style */
            """)

    def mousePressEvent(self, event):
        """Handle mouse press to select the tab."""
        if event.button() == Qt.LeftButton:
            self.selected.emit(self.index)
        super().mousePressEvent(event)


class Workspace(QWidget):
    """Main workspace area that displays content for the active tab."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {cp.BACKGROUND_DARK};
            }}
        """)

        # Use QStackedWidget to switch between different content views
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Default empty state
        self.empty_widget = self._create_empty_widget()
        self.stacked_widget.addWidget(self.empty_widget)

    def _create_empty_widget(self):
        """Create an empty state widget."""
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {cp.BACKGROUND_DARK};")

        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)

        # Icon/Logo
        icon_label = QLabel("TrajectoryLab")
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: {cp.BORDER_DIVIDER};
                font-size: 32px;
                font-weight: 300;
                font-family: "Segoe UI Light", "Roboto", sans-serif;
            }}
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Spacing
        layout.addSpacing(16)

        # Message
        label = QLabel("Select a file from the sidebar to get started")
        label.setStyleSheet(f"""
            QLabel {{
                color: {cp.SECONDARY_TEXT};
                font-size: 14px;
                font-family: "Segoe UI", "Roboto", sans-serif;
            }}
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        return widget

    def add_content(self, widget):
        """Add a content widget to the workspace."""
        index = self.stacked_widget.addWidget(widget)
        return index

    def show_content(self, index):
        """Show content at the given index."""
        if 0 <= index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(index)

    def remove_content(self, index):
        """Remove content at the given index."""
        if 0 <= index < self.stacked_widget.count():
            widget = self.stacked_widget.widget(index)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()

    def show_empty(self):
        """Show the empty state."""
        self.stacked_widget.setCurrentWidget(self.empty_widget)

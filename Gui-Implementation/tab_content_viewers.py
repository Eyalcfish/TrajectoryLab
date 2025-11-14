"""Content viewer widgets for displaying different file types in tabs."""

import json
import csv
from pathlib import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QLabel,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QAbstractScrollArea, QFrame, QScrollArea, QHBoxLayout, QPushButton, QPlainTextEdit, QTextEdit, QMessageBox)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QFont, QPainter, QColor, QTextCursor
import color_palette as cp


class LineNumberArea(QWidget):
    def __init__(self, settings_viewer):
        super().__init__(settings_viewer.editor)
        self.settings_viewer = settings_viewer

    def sizeHint(self):
        return QSize(self.settings_viewer.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.settings_viewer.lineNumberAreaPaintEvent(event)


class SettingsFileViewer(QWidget):
    """Editor for settings.json files."""
    profile_saved = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {cp.BACKGROUND_DARK};
            }}
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        self.editor.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {cp.BACKGROUND_DARK};
                color: {cp.PRIMARY_TEXT};
                border: none;
                padding: 16px 20px;
                font-family: "Consolas", "Courier New", monospace;
                line-height: 1.6;
            }}
            QScrollBar:vertical {{
                background: {cp.BACKGROUND_DARK};
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {cp.BORDER_DIVIDER};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {cp.INFO_HIGHLIGHT};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        self.lineNumberArea = LineNumberArea(self)

        layout.addWidget(self.lineNumberArea)
        layout.addWidget(self.editor)

        self.editor.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.editor.updateRequest.connect(self.updateLineNumberArea)
        self.editor.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addLayout(layout)

        # Bottom bar for save button and file path
        self.bottom_bar = self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar)
        self.setLayout(main_layout)

    def lineNumberAreaWidth(self):
        digits = 1
        max_num = max(1, self.editor.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.editor.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.editor.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(cp.BACKGROUND_DARK))

        block = self.editor.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top < event.rect().bottom() + self.fontMetrics().height():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor(cp.SECONDARY_TEXT))
                painter.drawText(0, int(top), self.lineNumberArea.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.editor.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(cp.BORDER_DIVIDER).lighter(160)
            selection.format.setBackground(lineColor)
            
            cursor = self.editor.textCursor()
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            selection.cursor = cursor
            extraSelections.append(selection)
        self.editor.setExtraSelections(extraSelections)

    def _create_bottom_bar(self):
        """Create the bottom bar with save button and file path."""
        container = QWidget()
        container.setFixedHeight(40)
        container.setStyleSheet(f"""
            background-color: {cp.CARD_SURFACE};
            border-top: 1px solid {cp.BORDER_DIVIDER};
        """)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(12)

        # File path label
        self.path_label = QLabel("No file loaded")
        self.path_label.setStyleSheet(f"""
            color: {cp.SECONDARY_TEXT};
            font-size: 11px;
            font-family: "Segoe UI", "Roboto", sans-serif;
            border: none;
        """)
        layout.addWidget(self.path_label)

        layout.addStretch()

        # Progress label
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"""
            color: {cp.PRIMARY_TEXT};
            font-size: 12px;
            font-weight: 600;
        """)
        layout.addWidget(self.progress_label)

        # Save button
        self.save_button = QPushButton("Save as New Profile")
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {cp.PRIMARY_BLUE};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {cp.PRIMARY_BLUE_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {cp.PRIMARY_BLUE_PRESSED};
            }}
            QPushButton:disabled {{
                background-color: {cp.BORDER_DIVIDER};
                color: {cp.SECONDARY_TEXT};
            }}
        """)
        self.save_button.clicked.connect(self.save_settings_file)
        layout.addWidget(self.save_button)

        return container

    def simulation_finished(self):
        """Called when the simulation is finished."""
        self.save_button.setEnabled(True)
        self.progress_label.setText("")

    def update_progress(self, value):
        """Update the progress label."""
        self.progress_label.setText(f"{value}%")

    def load_settings(self, settings_dict):
        """Load settings from a dictionary."""
        try:
            formatted_json = json.dumps(settings_dict, indent=2)
            self.editor.setPlainText(formatted_json)
        except Exception as e:
            self.editor.setPlainText(f"Error formatting settings: {e}")

    def load_settings_file(self, file_path):
        """Load settings from a JSON file."""
        self.file_path = file_path
        self.path_label.setText(str(self.file_path))
        try:
            with open(file_path, 'r') as f:
                settings = json.load(f)
            self.load_settings(settings)
        except FileNotFoundError:
            self.editor.setPlainText(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            self.editor.setPlainText(f"Invalid JSON: {e}")
        except Exception as e:
            self.editor.setPlainText(f"Error loading file: {e}")

    def _get_profile_num(self, p):
        """Safely get profile number from path."""
        try:
            return int(p.name.split('_')[-1])
        except (ValueError, IndexError):
            return -1

    def save_settings_file(self):
        """Save the current content as a new profile."""
        try:
            content = self.editor.toPlainText()
            # Validate if it's valid JSON before saving
            parsed_json = json.loads(content)

            # Find the next available profile number
            profile_dir = Path('profiles')
            profile_dir.mkdir(exist_ok=True)
            
            existing_profiles = [self._get_profile_num(p) for p in profile_dir.iterdir() if p.is_dir() and p.name.startswith('profile_')]
            valid_profiles = [p for p in existing_profiles if p != -1]
            
            next_profile_num = max(valid_profiles) + 1 if valid_profiles else 0
            
            new_profile_dir = profile_dir / f'profile_{next_profile_num}'
            new_profile_dir.mkdir(parents=True, exist_ok=True)

            new_settings_path = new_profile_dir / 'settings.json'
            with open(new_settings_path, 'w') as f:
                json.dump(parsed_json, f, indent=2)
            
            self.save_button.setEnabled(False)
            self.profile_saved.emit(str(new_settings_path))

        except json.JSONDecodeError:
            self.path_label.setText("Error: Invalid JSON format")
        except Exception as e:
            self.path_label.setText(f"Error saving file: {e}")


class CSVFileViewer(QWidget):
    """Viewer for displaying CSV files in a table."""
    profile_deleted = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {cp.BACKGROUND_DARK};
            }}
        """)

        # Main vertical layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Table widget
        self.table = QTableWidget()
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {cp.BACKGROUND_DARK};
                color: {cp.PRIMARY_TEXT};
                gridline-color: {cp.BORDER_DIVIDER};
                selection-background-color: {cp.PRIMARY_BLUE};
                selection-color: {cp.PRIMARY_TEXT};
                border: none;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 12px;
            }}
            QHeaderView::section {{
                background-color: {cp.CARD_SURFACE};
                color: {cp.PRIMARY_TEXT};
                font-weight: 600;
                padding: 10px 12px;
                border: none;
                border-right: 1px solid {cp.BORDER_DIVIDER};
                border-bottom: 1px solid {cp.BORDER_DIVIDER};
                font-family: "Segoe UI", "Roboto", sans-serif;
                font-size: 11px;
            }}
            QTableWidget::item {{
                padding: 8px 12px;
                border-bottom: 1px solid {cp.BORDER_DIVIDER};
            }}
            QScrollBar:vertical {{
                background: {cp.BACKGROUND_DARK};
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {cp.BORDER_DIVIDER};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {cp.INFO_HIGHLIGHT};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                background: {cp.BACKGROUND_DARK};
                height: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {cp.BORDER_DIVIDER};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {cp.INFO_HIGHLIGHT};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.table)
        
        self.header_text = "CSV File"
        
        # Bottom bar for delete button
        self.bottom_bar = self._create_bottom_bar()
        layout.addWidget(self.bottom_bar)

    def _create_bottom_bar(self):
        """Create the bottom bar with delete button."""
        container = QWidget()
        container.setFixedHeight(40)
        container.setStyleSheet(f"""
            background-color: {cp.CARD_SURFACE};
            border-top: 1px solid {cp.BORDER_DIVIDER};
        """)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(12)

        layout.addStretch()

        # Delete button
        self.delete_button = QPushButton("Delete Profile")
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.delete_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {cp.PRIMARY_RED};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {cp.PRIMARY_RED_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {cp.PRIMARY_RED_PRESSED};
            }}
        """)
        self.delete_button.clicked.connect(self.delete_profile)
        layout.addWidget(self.delete_button)

        return container

    def delete_profile(self):
        """Emit a signal to delete the profile."""
        if self.file_path:
            reply = QMessageBox.question(self, 'Delete Profile',
                                           "Are you sure you want to delete this profile?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.profile_deleted.emit(str(self.file_path))

    def load_csv_file(self, file_path, title=None):
        """Load and display a CSV file."""
        self.file_path = file_path
        try:
            if title:
                self.header_text = title
            else:
                self.header_text = f"CSV: {Path(file_path).name}"

            with open(file_path, newline='', encoding='utf-8') as f:
                reader = list(csv.reader(f))

                if not reader:
                    self._show_empty_message()
                    return

                # First row is headers
                headers = reader[0]
                rows = reader[1:]

                # Setup table
                self.table.setColumnCount(len(headers))
                self.table.setHorizontalHeaderLabels(headers)
                self.table.setRowCount(len(rows))

                # Populate table
                for r, row in enumerate(rows):
                    for c, val in enumerate(row):
                        item = QTableWidgetItem(val)
                        self.table.setItem(r, c, item)

                # Adjust column widths
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
                self.table.resizeColumnsToContents()

                # Set minimum column width
                for i in range(len(headers)):
                    if self.table.columnWidth(i) < 100:
                        self.table.setColumnWidth(i, 100)

        except FileNotFoundError:
            self._show_error_message(f"File not found: {file_path}")
        except Exception as e:
            self._show_error_message(f"Error loading CSV: {e}")

    def _show_empty_message(self):
        """Display message for empty CSV."""
        self.table.setRowCount(1)
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels([""])
        item = QTableWidgetItem("No data in CSV file")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(0, 0, item)

    def _show_error_message(self, message):
        """Display an error message in the table."""
        self.table.setRowCount(1)
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Error"])
        item = QTableWidgetItem(message)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(0, 0, item)


class PlaceholderViewer(QWidget):
    """Placeholder viewer for testing."""

    def __init__(self, title="Placeholder", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {cp.BACKGROUND_DARK};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)

        # Icon
        icon = QLabel("📄")
        icon.setStyleSheet(f"""
            QLabel {{
                font-size: 48px;
            }}
        """)
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        layout.addSpacing(16)

        # Title
        label = QLabel(title)
        label.setStyleSheet(f"""
            QLabel {{
                color: {cp.PRIMARY_TEXT};
                font-size: 18px;
                font-weight: 600;
                font-family: "Segoe UI", "Roboto", sans-serif;
            }}
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        layout.addSpacing(8)

        # Description
        desc = QLabel("This content is ready to be displayed")
        desc.setStyleSheet(f"""
            QLabel {{
                color: {cp.SECONDARY_TEXT};
                font-size: 13px;
                font-family: "Segoe UI", "Roboto", sans-serif;
            }}
        """)
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

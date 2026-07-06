# ==============================================================================
# SCRIPT: SubVoid+.py
# VERSION: 2026.07.06__15.48.18
# TARGET: Python 3.14.5
#
# Copyright (C) 2026 pwshAgyjkcrg761
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
# ==============================================================================
# <PROTECTED>
# ==============================================================================
# AI INSTRUCTIONS v2026.06.24__06.54.45 : 
#
# 1. MESSAGE STAMP: 
#    - Every response containing code MUST begin with a standalone version stamp.
#    - Use CHICAGO TIME (Central Time), 24-hour clock.
#    - Format: YYYY.MM.DD__HH.MM.SS.
#    - CRITICAL: Use the time provided in the prompt or at https://www.timeanddate.com/worldclock/usa/chicago. Ensure minutes are exact.
#
# 2. VERSION SNIPPET PROHIBITION:
#    - DO NOT provide code snippets, anchors, or steps to update the script's internal VERSION comment or $scriptVersion variable. 
#    - The user handles internal file versioning manually based on the Message Stamp.
#
# 3. SCRIPT OUTPUT (SURGICAL FIXES ONLY):
#    - Provide minimal, highly targeted, surgical edits. Do not rewrite large blocks or entire functions.
#    - Always use a codebox with a copy button.
#    - Multiple modifications MUST be presented strictly ONE step at a time. Wait for user confirmation before proceeding to the next step. 
#    - DO NOT modify or refactor any code inside <PROTECTED> tags.
#
# 4. VERBATIM ANCHOR PROTOCOL (FOR NOTEPAD++):
#    - To facilitate "Find" in Notepad++, always structure edits with:
#      - "Verbatim Anchor (Before)" - The exact lines of existing code immediately before the change.
#      - "Verbatim Anchor (After)" - The exact lines of existing code immediately after the change.
#      - "Snippet to REPLACE" - The exact code block to be deleted.
#      - "What to PASTE in its place" - The new code block to be inserted.
#    - Do not summarize, truncate, or refactor the existing code used as an anchor.
#    - Match spaces, comments, and symbols exactly as they appear in the file.
#
# 5. CONTENT PRESERVATION:
#    - Do not remove, modify, or strip out telemetry data or DevDebug information from any provided code.
#==============================================================================
#==============================================================================
# </PROTECTED>

import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QFileDialog, QLineEdit, QLabel, 
                             QMessageBox, QPlainTextEdit)
from PyQt6.QtGui import QActionGroup, QPalette, QColor

# Easily maintainable application metadata configuration
APP_VERSION = "2026.07.06__15.48.18"

class SettingsWrapper:
    def __init__(self, config_path):
        self.path = config_path
        self.data = {}
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    self.data = json.load(f)
            except: pass
    def value(self, key, default):
        return self.data.get(key, default)
    def setValue(self, key, value):
        self.data[key] = value
        with open(self.path, 'w') as f:
            json.dump(self.data, f)



class SubtitleEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"SubVoid+ v{APP_VERSION}")
        
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.config_file = os.path.join(script_dir, "SubVoid+.config.json")
        self.default_size = (500, 250)
        
        # Load persistent settings
        self.settings = SettingsWrapper(self.config_file)
        self.load_geometry()
        
        # Load and apply theme immediately
        self.current_theme = self.settings.value("theme", "System")
        self.apply_theme(self.current_theme)
        self.last_directory = os.path.normpath(self.settings.value("last_directory", os.getcwd()))
        
        self.init_ui()
        self.load_saved_settings()
        self.update_output_display()

    def init_ui(self):
        self.create_menu()
        layout = QVBoxLayout()
        
        # Directory Selection
        self.dir_label = QLabel(f"Selected Folder: {self.last_directory}")
        layout.addWidget(self.dir_label)
        
        self.output_label = QLabel()
        self.output_label.setWordWrap(True)
        layout.addWidget(self.output_label)
        
        btn_select = QPushButton("Select Folder")
        btn_select.clicked.connect(self.select_directory)
        layout.addWidget(btn_select)
        
        # Find and Replace Inputs
        self.input_find = QPlainTextEdit()
        self.input_find.setPlaceholderText("Find text (one per line)...")
        self.input_find.setMaximumHeight(100)
        layout.addWidget(self.input_find)
        
        self.input_replace = QLineEdit()
        self.input_replace.setPlaceholderText("Replace with...")
        layout.addWidget(self.input_replace)
        
        # Process Button
        btn_run = QPushButton("Process Subtitles")
        btn_run.clicked.connect(self.run_process)
        layout.addWidget(btn_run)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def load_saved_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.input_find.setPlainText(config.get("find_text", ""))
                    self.input_replace.setText(config.get("replace_text", ""))
            except:
                pass

    def update_output_display(self):
        clean_dir = os.path.normpath(self.last_directory)
        parent_dir = os.path.dirname(clean_dir)
        folder_name = os.path.basename(clean_dir)
        # Force conversion to OS-native separators
        output_dir = os.path.normpath(os.path.join(parent_dir, f"{folder_name}_updated-SubVoid+"))
        self.output_label.setText(f"Output will be saved to: {output_dir}")

    def load_geometry(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.move(config.get("x", 100), config.get("y", 100))
                    self.resize(config.get("width", self.default_size[0]),
                                config.get("height", self.default_size[1]))
            except:
                self.resize(*self.default_size)
        else:
            self.resize(*self.default_size)

    def closeEvent(self, event):
        # Save window position and size
        pos = self.pos()
        self.settings.setValue("x", pos.x())
        self.settings.setValue("y", pos.y())
        self.settings.setValue("width", self.width())
        self.settings.setValue("height", self.height())
        self.settings.setValue("find_text", self.input_find.toPlainText())
        self.settings.setValue("replace_text", self.input_replace.text())
        self.settings.setValue("theme", self.current_theme)
        event.accept()

    

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", self.last_directory)
        if dir_path:
            # Force system-native separators
            self.last_directory = os.path.normpath(dir_path).replace('/', os.sep)
            self.dir_label.setText(f"Selected Folder: {self.last_directory}")
            self.settings.setValue("last_directory", self.last_directory)
            self.update_output_display()
            
    def create_menu(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("&File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        tools_menu = menu_bar.addMenu("&Tools")
        themes_menu = tools_menu.addMenu("&Themes")
        
        # Theme selection setup
        self.theme_group = QActionGroup(self)
        self.theme_group.setExclusive(True)
        
        themes = ["Dark", "Light", "System"]
        for theme in themes:
            action = themes_menu.addAction(theme)
            action.setCheckable(True)
            self.theme_group.addAction(action)
            action.triggered.connect(lambda checked, t=theme: self.change_theme(t))
            
        # Set default based on saved setting
        saved_theme = self.settings.value("theme", "System")
        for action in self.theme_group.actions():
            if action.text() == saved_theme:
                action.setChecked(True)
        
        help_menu = menu_bar.addMenu("&Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

    def change_theme(self, theme_name):
        print(f"Theme changed to: {theme_name}")
        
    def apply_theme(self, theme_name):
        app = QApplication.instance()
        app.setStyle("Fusion")
        palette = QPalette()
        
        if theme_name == "Dark":
            palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#2d2d2d"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#1e1e1e"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#252526"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#333333"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#aaaaaa"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#007acc"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor("#666666"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#666666"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor("#666666"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor("#1e1e1e"))
            
        elif theme_name == "Light":
            palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#fcfcfc"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#e1e1e1"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#777777"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#0078d7"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor("#a0a0a0"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#a0a0a0"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor("#a0a0a0"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor("#e1e1e1"))
            
        else: # System
            is_dark = app.style().standardPalette().color(QPalette.ColorRole.Window).lightness() < 128
            self.apply_theme("Dark" if is_dark else "Light")
            return
            
        app.setPalette(palette)

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme(theme_name)

    def show_about(self):
        about_text = (
            f"<b>SubVoid+ v{APP_VERSION}</b><br>"
            "Copyright (C) 2026 pwshAgyjkcrg761<br>"
            "GPLv3<br><br>"
            "This program is free software: you can redistribute it and/or modify "
            "it under the terms of the GNU General Public License as published by "
            "the Free Software Foundation, either version 3 of the License, or "
            "(at your option) any later version.<br><br>"
            "This program is distributed in the hope that it will be useful, "
            "but WITHOUT ANY WARRANTY; without even the implied warranty of "
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the "
            "GNU General Public License for more details.<br><br>"
            "You should have received a copy of the GNU General Public License "
            "along with this program. If not, see "
            "<a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">https://www.gnu.org/licenses/gpl-3.0.html</a>."
        )
        QMessageBox.about(self, "About", about_text)

    def run_process(self):
        full_find_text = self.input_find.toPlainText()
        find_terms = [line.strip() for line in full_find_text.splitlines() if line.strip()]
        replace_text = self.input_replace.text()
        
        if not find_terms:
            QMessageBox.warning(self, "Input Required", "Please enter text to find.")
            return

        clean_dir = os.path.normpath(self.last_directory)
        parent_dir = os.path.dirname(clean_dir)
        folder_name = os.path.basename(clean_dir)
        output_dir = os.path.normpath(os.path.join(parent_dir, f"{folder_name}_updated-SubVoid+"))
        os.makedirs(output_dir, exist_ok=True)
        
        count = 0
        for filename in os.listdir(self.last_directory):
            if filename.endswith((".srt", ".ass", ".ssa")):
                file_path = os.path.join(self.last_directory, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    
                    modified = False
                    for term in find_terms:
                        if term in content:
                            content = content.replace(term, replace_text)
                            modified = True
                    
                    if modified:
                        new_file_path = os.path.join(output_dir, filename)
                        with open(new_file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        QMessageBox.information(self, "Complete", f"Processed {count} files.\n\nSaved to: {output_dir}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SubtitleEditor()
    window.show()
    sys.exit(app.exec())
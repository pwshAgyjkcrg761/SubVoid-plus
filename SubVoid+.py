# ==============================================================================
# SCRIPT: SubVoid+.py
# VERSION: 2026.07.11__15.41.51
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
# AI INSTRUCTIONS
# Copyright (c) 2026 pwshAgyjkcrg761
# License: MIT
# Source: https://codeberg.org/pwshAgyjkcrg761/AI_Instructions
#
# AI INSTRUCTIONS v2026.07.11__15.41.51 : 
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
# ==============================================================================
# </PROTECTED>

import sys
import os
import json
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QFileDialog, QLineEdit, QLabel, 
                             QMessageBox, QPlainTextEdit, QDialog, QCheckBox,
                             QTextBrowser)
from PyQt6.QtGui import QActionGroup, QPalette, QColor, QIcon
import ctypes

# Easily maintainable application metadata configuration
APP_VERSION = "2026.07.11__15.41.51"

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
        
        # Ensure the internal directory exists and place config inside it
        internal_dir = os.path.join(script_dir, "SubVoid+_internal")
        os.makedirs(internal_dir, exist_ok=True)
        self.config_file = os.path.join(internal_dir, "SubVoid+.config.json")
        
        # Set taskbar and titlebar icon from the internal path
        icon_path = os.path.join(internal_dir, "Subvoid+_icon", "SubVoid+-vortex-indigo-icon.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        # Fix taskbar icon grouping for Windows environments
        if sys.platform == "win32":
            myappid = f"pwshAgyjkcrg761.subvoidplus.{APP_VERSION}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.default_size = (600, 350)
        
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
        
        self.check_case = QCheckBox("Case Sensitive Find")
        self.check_case.setToolTip("Enforce strict character case matching during search operations.")
        layout.addWidget(self.check_case)
        
        self.check_purge = QCheckBox("Delete Lines with Matches")
        self.check_purge.setToolTip("Completely strip the entire text payload from a line if any search term matches it.")
        layout.addWidget(self.check_purge)

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
        self.resize(*self.default_size)
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    if "x" in config and "y" in config:
                        self.move(config.get("x"), config.get("y"))
                    else:
                        self.center_window()
                    self.resize(config.get("width", self.default_size[0]),
                                config.get("height", self.default_size[1]))
            except:
                self.center_window()
        else:
            self.center_window()

    def center_window(self):
        frame_geo = self.frameGeometry()
        screen = QApplication.primaryScreen().availableGeometry().center()
        frame_geo.moveCenter(screen)
        self.move(frame_geo.topLeft())

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
        filter_action = tools_menu.addAction("Filters")
        filter_action.triggered.connect(self.show_filters)
        
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

    def show_filters(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Filters")
        layout = QVBoxLayout()
        
        check_ads = QCheckBox("Remove ad-related lines (http/https/.com/.net/.org)")
        check_ads.setChecked(self.settings.value("filter_ads", False))
        check_ads.stateChanged.connect(lambda state: self.settings.setValue("filter_ads", state == 2))
        
        layout.addWidget(check_ads)
        
        check_tags = QCheckBox("Remove hashtag lines (#tags)")
        check_tags.setChecked(self.settings.value("filter_tags", False))
        check_tags.stateChanged.connect(lambda state: self.settings.setValue("filter_tags", state == 2))
        layout.addWidget(check_tags)
        
        check_spam = QCheckBox("Remove Donation && Contact Spam (Crypto, Emails, Cards)")
        check_spam.setChecked(self.settings.value("filter_spam", False))
        check_spam.stateChanged.connect(lambda state: self.settings.setValue("filter_spam", state == 2))
        layout.addWidget(check_spam)
        
        check_recruits = QCheckBox("Remove Recruitment && Sub Promotional Lines")
        check_recruits.setChecked(self.settings.value("filter_recruits", False))
        check_recruits.stateChanged.connect(lambda state: self.settings.setValue("filter_recruits", state == 2))
        layout.addWidget(check_recruits)
        dialog.setLayout(layout)
        dialog.exec()

    def show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About")
        dialog.resize(420, 320)
        
        layout = QVBoxLayout(dialog)
        
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        
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
            "<a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">https://www.gnu.org/licenses/gpl-3.0.html</a>.<br><br>"
            "<hr><br>"
            "<b>Icon Credits:</b><br>"
            "'Tornado SVG Vector' (SubVoid+-vortex-indigo-icon.svg) by JoyPixels via <a href=\"https://www.svgrepo.com/svg/402817/tornado\">SVGRepo</a>.<br>"
            "Used under MIT License. Modified by pwshAgyjkcrg761 (Color/Format)."
        )
        text_browser.setHtml(about_text)
        layout.addWidget(text_browser)
        
        from PyQt6.QtWidgets import QHBoxLayout
        
        # Path configuration to the icon license folder
        script_dir = os.path.dirname(os.path.realpath(__file__))
        license_folder = os.path.join(script_dir, "SubVoid+_internal", "Subvoid+_icon")
        
        def open_license_folder():
            if os.path.exists(license_folder):
                os.startfile(license_folder) if sys.platform == "win32" else os.system(f'xdg-open "{license_folder}"')
        
        # Horizontal layout row for the action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Pushes everything to the right side
        
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(dialog.accept)
        button_layout.addWidget(btn_ok)
        
        btn_license = QPushButton("View Icon License")
        btn_license.clicked.connect(open_license_folder)
        button_layout.addWidget(btn_license)
        
        layout.addLayout(button_layout)
        
        dialog.exec()

    def run_process(self):
        full_find_text = self.input_find.toPlainText()
        find_terms = [line.strip() for line in full_find_text.splitlines() if line.strip()]
        replace_text = self.input_replace.text()
        
        filter_ads_enabled = self.settings.value("filter_ads", False)
        filter_tags_enabled = self.settings.value("filter_tags", False)
        filter_spam_enabled = self.settings.value("filter_spam", False)
        filter_recruits_enabled = self.settings.value("filter_recruits", False)
        
        if not find_terms and not filter_ads_enabled and not filter_tags_enabled and not filter_spam_enabled and not filter_recruits_enabled:
            QMessageBox.warning(self, "Input Required", "Please enter text to find or enable a filter configuration.")
            return

        clean_dir = os.path.normpath(self.last_directory)
        parent_dir = os.path.dirname(clean_dir)
        folder_name = os.path.basename(clean_dir)
        output_dir = os.path.normpath(os.path.join(parent_dir, f"{folder_name}_updated-SubVoid+"))
        os.makedirs(output_dir, exist_ok=True)
        
        # Pre-compile patterns
        tag_pattern = re.compile(r'#\S')
        ad_pattern = re.compile(r'https?://|\w+\.(?:com|net|org)\b', re.IGNORECASE)
        
        # Matches email addresses, 4x4 credit card groups, crypto wallet indicators, or payment keywords
        spam_pattern = re.compile(
            r'[\w\.-]+@[\w\.-]+\.\w+|'                    # Emails
            r'\b\d{4}[ \t]\d{4}[ \t]\d{4}[ \t]\d{4}\b|'    # CC numbers (4x4 digits)
            r'\b0x[a-fA-F0-9]{40}\b|'                      # Ethereum hex addresses
            r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|'        # Bitcoin legacy/P2SH addresses
            r'\b(?:Eth|BitC|Paypal|Yandex|WebMoney|QIWI):', # Payment keyword prefixes
            re.IGNORECASE
        )
        
        # Matches fansub crew recruitment blocks and subscription/donation introductory phrases safely
        recruit_pattern = re.compile(
            r'sub\s+for\s+us|'
            r'please\s+contact\s+us|'
            r'expand\s+our\s+services\s+we\s+need\s+your\s+help|'
            r'grateful\s+for\s+your\s+contributions|'
            r'if\s+you\'re\s+(?:translator|editor|tlc|raw-provider|uploader|sponsor|typesetter)|'
            r'raw-provider\s+or\s+sponsor|' # Captures broken multi-line split variants
            r'contact\s+us!',
            re.IGNORECASE
        )
        
        count = 0
        for filename in os.listdir(self.last_directory):
            if filename.endswith((".srt", ".ass", ".ssa")):
                file_path = os.path.join(self.last_directory, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        original_content = f.read()
                    
                    content = original_content
                    is_ass_ssa = filename.lower().endswith((".ass", ".ssa"))
                    is_srt = filename.lower().endswith(".srt")
                    
                    input_lines = content.splitlines()
                    total_lines = len(input_lines)
                    skip_indices = set()
                    
                    role_regex = re.compile(r'if\s+you\'re\s+(?:translator|editor|tlc|raw-provider|uploader|sponsor|typesetter)', re.IGNORECASE)
                    contact_regex = re.compile(r'contact\s+us', re.IGNORECASE)
                    srt_time_pattern = re.compile(r'^\d+:\d+:\d+[\.,]\d+\s*-->\s*\d+:\d+:\d+[\.,]\d+$')
                    
                    # Helper function to extract text payload from any given line index safely
                    def get_line_payload(idx):
                        if idx < 0 or idx >= total_lines:
                            return None, False
                        l_text = input_lines[idx]
                        cleaned_l = l_text.strip()
                        if is_ass_ssa:
                            if ":" in l_text:
                                tag, payload = l_text.split(":", 1)
                                if tag.strip().lower() in ("dialogue", "comment"):
                                    parts = payload.split(",", 9)
                                    return (parts[9] if len(parts) == 10 else payload), True
                        elif is_srt:
                            if cleaned_l != "" and not cleaned_l.isdigit() and not srt_time_pattern.match(cleaned_l):
                                return l_text, True
                        return None, False

                    # Pass 1: Multi-line adjacent tracking logic (Check 1 line above or below for role + contact combos)
                    if filter_recruits_enabled:
                        for idx in range(total_lines):
                            sub_text, is_eligible = get_line_payload(idx)
                            if is_eligible and role_regex.search(sub_text):
                                # Check 1 line above if it is eligible dialogue/text
                                prev_text, prev_eligible = get_line_payload(idx - 1)
                                if prev_eligible and contact_regex.search(prev_text):
                                    skip_indices.add(idx)
                                    skip_indices.add(idx - 1)
                                # Check 1 line below if it is eligible dialogue/text
                                next_text, next_eligible = get_line_payload(idx + 1)
                                if next_eligible and contact_regex.search(next_text):
                                    skip_indices.add(idx)
                                    skip_indices.add(idx + 1)

                    # Pass 2: Line Parsing and Content Substitutions / Stripping
                    protected_lines = []
                    in_events_section = False
                    
                    for idx in range(total_lines):
                        line = input_lines[idx]
                        cleaned_line = line.strip()
                        
                        # Section tracking for ASS/SSA structures
                        if is_ass_ssa:
                            if cleaned_line.lower() == "[events]":
                                in_events_section = True
                                protected_lines.append(line)
                                continue
                            elif cleaned_line.startswith("[") and cleaned_line.endswith("]"):
                                in_events_section = False
                                protected_lines.append(line)
                                continue

                        # Classify line components to check if content scanning is allowed
                        is_eligible_content = False
                        sub_text = line
                        parts = []
                        tag = ""
                        
                        if is_ass_ssa and ":" in line:
                            tag, payload = line.split(":", 1)
                            if in_events_section and tag.strip().lower() in ("dialogue", "comment"):
                                is_eligible_content = True
                                parts = payload.split(",", 9)
                                if len(parts) == 10:
                                    sub_text = parts[9]
                                else:
                                    sub_text = payload
                        elif is_srt:
                            if not cleaned_line.isdigit() and not srt_time_pattern.match(cleaned_line) and cleaned_line != "":
                                is_eligible_content = True

                        # Handle Automated Filters (Stripping onscreen text only)
                        if is_eligible_content:
                            if is_ass_ssa and cleaned_line.startswith(";"):
                                pass  # Avoid touching native file comments
                            else:
                                is_spam_ad = False
                                if idx in skip_indices:
                                    is_spam_ad = True
                                elif filter_ads_enabled and ad_pattern.search(sub_text):
                                    is_spam_ad = True
                                elif filter_tags_enabled and tag_pattern.search(sub_text):
                                    is_spam_ad = True
                                elif filter_spam_enabled and spam_pattern.search(sub_text):
                                    is_spam_ad = True
                                elif filter_recruits_enabled and recruit_pattern.search(sub_text):
                                    is_spam_ad = True
                                    
                                if is_spam_ad:
                                    sub_text = ""

                        # Handle manual user find/replace modifications securely inside text payload segments
                        if find_terms and is_eligible_content and sub_text != "":
                            flags = 0 if self.check_case.isChecked() else re.IGNORECASE
                            for term in find_terms:
                                term_pattern = re.compile(re.escape(term), flags)
                                if term_pattern.search(sub_text):
                                    if self.check_purge.isChecked():
                                        sub_text = ""
                                        break
                                    else:
                                        sub_text = term_pattern.sub(replace_text, sub_text)

                        # Re-aggregate text segment back into the original line structure
                        if is_eligible_content:
                            if is_ass_ssa:
                                if len(parts) == 10:
                                    parts[9] = sub_text
                                    line = f"{tag}:{','.join(parts)}"
                                else:
                                    line = f"{tag}:{sub_text}"
                            elif is_srt:
                                line = sub_text

                        protected_lines.append(line)
                        
                    content = "\n".join(protected_lines)
                    modified = (content != original_content)
                    
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
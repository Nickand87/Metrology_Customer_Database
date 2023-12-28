import os
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QMessageBox
from gui import ClientWindow, SettingsWindow  # Assuming ClientWindow is a QWidget subclass defined in another file
from db_control import DatabaseManager
import xml.etree.ElementTree as ET
from styles import dark_style, light_style
import qdarkstyle


class MainWindow(QMainWindow):
    """Main window of the application."""
    def __init__(self, db_manager):
        super().__init__()
        self.setWindowTitle("Dynamic UI Application")
        self.setGeometry(100, 100, 800, 600)
        self.db_manager = db_manager
        self.setup_ui()

    def setup_ui(self):
        """Setup the UI components."""
        main_layout = QHBoxLayout()
        sidebar_layout = QVBoxLayout()

        self.button1 = QPushButton("Clients")
        self.button1.clicked.connect(lambda: self.switch_page(0))
        sidebar_layout.addWidget(self.button1)

        self.button2 = QPushButton("Settings")
        self.button2.clicked.connect(lambda: self.switch_page(1))
        sidebar_layout.addWidget(self.button2)

        sidebar_layout.addStretch()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(ClientWindow(self.db_manager))
        self.stacked_widget.addWidget(SettingsWindow(self.db_manager))

        main_layout.addLayout(sidebar_layout, 1)
        main_layout.addWidget(self.stacked_widget, 4)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def switch_page(self, page_index):
        """Switch between pages in the stacked widget."""
        self.stacked_widget.setCurrentIndex(page_index)


def read_db_path_from_settings():
    """Read the database path from the XML settings file."""
    try:
        tree = ET.parse('settings.xml')
        root = tree.getroot()
        db_path = root.find('database/path').text
        return db_path
    except ET.ParseError:
        QMessageBox.critical(None, "Error", "Error parsing settings.xml.")
        sys.exit(1)
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error reading settings: {str(e)}")
        sys.exit(1)


def read_style_setting():
    """Read the style setting from settings.xml."""
    try:
        tree = ET.parse('settings.xml')
        root = tree.getroot()
        return root.find('style/selection').text
    except Exception:
        return None  # Return None if the setting is not found


def apply_style(app, style_name):
    """Apply the selected style to the application."""
    if style_name == "dark":
        app.setStyleSheet(dark_style())
    elif style_name == "light":
        app.setStyleSheet(light_style())
    else:
        app.setStyleSheet("")  # Apply default style if the name is not recognized


def main():
    """Main function to start the application."""
    app = QApplication(sys.argv)

    style_setting = read_style_setting()
    apply_style(app, style_setting)  # Apply the style at the start of the application

    db_directory = read_db_path_from_settings()
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
    db_path = os.path.join(db_directory, "customer_info.db")

    db_manager = DatabaseManager(db_path)
    mainWin = MainWindow(db_manager)
    mainWin.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
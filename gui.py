from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QFormLayout, QListWidgetItem, QFrame, QMessageBox
from PyQt5.QtGui import QFont, QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
import xml.etree.ElementTree as ET
import qdarkstyle
from styles import dark_style, light_style
import sys
import random
from db_control import DatabaseManager


class ClientWindow(QMainWindow):

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.initializeUI()
        self.view_customers()

    def initializeUI(self):
        self.setWindowTitle("Customer Information")
        self.setGeometry(100, 100, 800, 500)
        #self.setStyleSheet(qdarkstyle.load_stylesheet())

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.setupIDFrame(main_layout)
        self.setupInputFields(main_layout)
        self.setupButtons(main_layout)
        self.setupCustomerList(main_layout)

    def setupIDFrame(self, layout):
        id_frame = QFrame()
        id_frame.setFrameShape(QFrame.StyledPanel)
        id_layout = QHBoxLayout(id_frame)
        layout.addWidget(id_frame)

        font = QFont("Arial", 12)
        label_font = QFont("Arial", 10, QFont.Bold)

        self.client_id_entry = QLineEdit()
        self.client_id_entry.setValidator(QIntValidator())
        self.client_id_entry.setFont(font)

        id_label = QLabel("ID:")
        id_label.setFont(label_font)

        id_layout.addWidget(id_label)
        id_layout.addWidget(self.client_id_entry)

    def setupInputFields(self, layout):
        input_layout = QHBoxLayout()
        layout.addLayout(input_layout)

        self.setupCompanyInfo(input_layout)
        self.setupContacts(input_layout)

    def setupCompanyInfo(self, layout):
        company_info_frame = QFrame()
        company_info_frame.setFrameShape(QFrame.StyledPanel)
        company_info_layout = QFormLayout(company_info_frame)
        layout.addWidget(company_info_frame)

        font = QFont("Arial", 12)
        label_font = QFont("Arial", 10, QFont.Bold)

        company_info_title = QLabel("Company Info")
        company_info_title.setFont(label_font)
        company_info_layout.addRow(company_info_title)

        self.client_name_entry = QLineEdit()
        self.client_address1_entry = QLineEdit()
        self.client_address2_entry = QLineEdit()
        self.client_phone_entry = QLineEdit()
        self.client_emailfax_entry = QLineEdit()

        phone_reg_exp = QRegExp("[0-9\-]+")
        self.client_phone_entry.setValidator(QRegExpValidator(phone_reg_exp))

        for label_text, widget in [
            ("Customer Name:", self.client_name_entry),
            ("Address:", self.client_address1_entry),
            ("Address:", self.client_address2_entry),
            ("Phone #:", self.client_phone_entry),
            ("Email/Fax:", self.client_emailfax_entry)
        ]:
            label = QLabel(label_text)
            label.setFont(label_font)
            widget.setFont(font)
            company_info_layout.addRow(label, widget)

    def setupContacts(self, layout):
        contacts_frame = QFrame()
        contacts_frame.setFrameShape(QFrame.StyledPanel)
        contacts_layout = QFormLayout(contacts_frame)
        layout.addWidget(contacts_frame)

        font = QFont("Arial", 12)
        label_font = QFont("Arial", 10, QFont.Bold)

        contacts_title = QLabel("Contacts")
        contacts_title.setFont(label_font)
        contacts_layout.addRow(contacts_title)

        self.contact_name_entry = QLineEdit()
        self.contact_address1_entry = QLineEdit()
        self.contact_address2_entry = QLineEdit()
        self.contact_phone_entry = QLineEdit()
        self.contact_emailfax_entry = QLineEdit()

        phone_reg_exp = QRegExp("[0-9\-]+")
        self.contact_phone_entry.setValidator(QRegExpValidator(phone_reg_exp))

        for label_text, widget in [
            ("Contact Name:", self.contact_name_entry),
            ("Address:", self.contact_address1_entry),
            ("Address:", self.contact_address2_entry),
            ("Phone #:", self.contact_phone_entry),
            ("Email/Fax:", self.contact_emailfax_entry)
        ]:
            label = QLabel(label_text)
            label.setFont(label_font)
            widget.setFont(font)
            contacts_layout.addRow(label, widget)

    def setupButtons(self, layout):
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        font = QFont("Arial", 12)

        self.submit_button = QPushButton("Submit")
        self.load_button = QPushButton("Load Customer")
        self.delete_button = QPushButton("Delete Customer")
        self.clear_button = QPushButton("Clear Fields")

        self.submit_button.setFont(font)
        self.load_button.setFont(font)
        self.delete_button.setFont(font)
        self.clear_button.setFont(font)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)

    def setupCustomerList(self, layout):
        self.customer_list = QListWidget()
        self.customer_list.setAlternatingRowColors(True)
        layout.addWidget(self.customer_list)

    def view_customers(self):
        self.db_manager.cursor.execute("SELECT customer_id, customer_name, customer_address1 FROM customers")
        all_customers = self.db_manager.cursor.fetchall()
        self.customer_list.clear()
        for customer in all_customers:
            self.customer_list.addItem(f"{customer[0]}: {customer[1]}: {customer[2]}")


class SettingsWindow(QMainWindow):

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet(qdarkstyle.load_stylesheet())

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Database Path Setting
        db_path_layout = QHBoxLayout()
        self.db_path_label = QLabel("Database Path:")
        self.db_path_entry = QLineEdit()
        db_path_layout.addWidget(self.db_path_label)
        db_path_layout.addWidget(self.db_path_entry)
        layout.addLayout(db_path_layout)

        # Style Selection Setting
        style_layout = QHBoxLayout()
        self.style_label = QLabel("Style Selection:")
        self.style_entry = QLineEdit()
        style_layout.addWidget(self.style_label)
        style_layout.addWidget(self.style_entry)
        layout.addLayout(style_layout)

        # Load current settings
        self.load_settings()

        # Save Button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        def apply_style(self, style_name):
            """Apply the selected style to the application."""
            if style_name == "dark":
                self.setStyleSheet(dark_style)
            elif style_name == "light":
                self.setStyleSheet(light_style)
            else:
                self.setStyleSheet("")  # Default style

    def load_settings(self):
        """Load settings from the XML file and update the UI."""
        try:
            tree = ET.parse('settings.xml')
            root = tree.getroot()
            db_path = root.find('database/path').text
            style_selection = root.find('style/selection').text
            self.db_path_entry.setText(db_path)
            self.style_entry.setText(style_selection)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading settings: {str(e)}")

    def save_settings(self):
        """Save the settings to the XML file."""
        try:
            tree = ET.parse('settings.xml')
            root = tree.getroot()
            root.find('database/path').text = self.db_path_entry.text()
            style_selection = self.style_entry.text()
            root.find('style/selection').text = style_selection
            tree.write('settings.xml')

            self.apply_style(style_selection)  # Apply the selected style

            QMessageBox.information(self, "Success", "Settings saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving settings: {str(e)}")


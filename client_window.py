from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QListWidget, QFormLayout, QListWidgetItem, QFrame, QMessageBox
from PyQt5.QtGui import QFont, QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
import qdarktheme
import random


class ClientWindow(QMainWindow):

    def __init__(self, conn, c):
        super().__init__()
        self.conn = conn
        self.c = c
        self.initializeUI()
        self.view_customers(c)

    def initializeUI(self):
        self.setWindowTitle("Customer Information")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet(qdarktheme.load_stylesheet())

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
        layout.addWidget(self.customer_list)
        self.customer_list.setStyleSheet("alternate-background-color: #505050;")
        self.customer_list.setAlternatingRowColors(True)

    def view_customers(self, c):
        c.execute("SELECT customer_id, customer_name, customer_address1 FROM customers")
        all_customers = c.fetchall()
        self.customer_list.clear()
        for customer in all_customers:
            self.customer_list.addItem(f"{customer[0]}: {customer[1]}: {customer[2]}")
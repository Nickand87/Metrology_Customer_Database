from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QListWidget, QFormLayout, QListWidgetItem, QFrame, QMessageBox
from PyQt5.QtGui import QFont, QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
import qdarktheme
import random


class ClientWindow(QMainWindow):

    def submit_action(self):
        customer_id = self.customer_id_entry.text()
        customer_name = self.customer_name_entry.text()
        customer_address1 = self.customer_address1_entry.text()
        customer_address2 = self.customer_address2_entry.text()
        customer_phone = self.customer_phone_entry.text()
        customer_email_fax = self.customer_emailfax_entry.text()

        if customer_id:
            self.c.execute("UPDATE customers SET customer_name=?, customer_address1=?, customer_address2=?, customer_emailfax=?, customer_phone=? WHERE customer_id=?",
                      (customer_name, customer_address1, customer_address2, customer_email_fax, customer_phone, customer_id))
        else:
            while True:
                new_id = random.randint(100000, 999999)
                self.c.execute("SELECT customer_id FROM customers WHERE customer_id=?", (new_id,))
                if not self.c.fetchone():
                    break

            self.c.execute("INSERT INTO customers (customer_id, customer_name, customer_address1, customer_address2, customer_emailfax, customer_phone) VALUES (?, ?, ?, ?, ?, ?)",
                      (new_id, customer_name, customer_address1, customer_address2, customer_email_fax, customer_phone))

        self.conn.commit()
        QMessageBox.information(self, "Submitted", f"Information Submitted for {customer_name}")
        self.view_customers(self)

    def view_customers(self):
        self.c.execute("SELECT customer_id, customer_name, customer_address1 FROM customers")
        all_customers = self.c.fetchall()
        self.customer_list.clear()
        for customer in all_customers:
            self.customer_list.addItem(f"{customer[0]}: {customer[1]}: {customer[2]}")

    def delete_customer(self):
        selected_item = self.customer_list.selectedItems()
        if selected_item:
            customer_id = selected_item[0].text().split(':')[0]
            self.c.execute("DELETE FROM customers WHERE customer_id=?", (customer_id,))
            self.conn.commit()
            self.view_customers(self)
            self.clear_entries(self)
        else:
            QMessageBox.critical(self, "Error", "No customer selected")

    def clear_entries(self):
        self.customer_id_entry.setReadOnly(False)
        self.customer_id_entry.clear()
        self.customer_id_entry.setReadOnly(True)
        self.customer_name_entry.clear()
        self.customer_address1_entry.clear()
        self.customer_address2_entry.clear()
        self.customer_phone_entry.clear()
        self.customer_emailfax_entry.clear()

    def __init__(self, conn, c):
        super().__init__()
        self.conn = conn
        self.c = c
        self.setWindowTitle("Customer Information")
        self.setGeometry(100, 100, 800, 500)  # Adjusted window size



        # Set style sheets
        darktheme_stylesheet = qdarktheme.load_stylesheet()

        # Central Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QVBoxLayout(central_widget)

        # Font Settings
        font = QFont("Arial", 12)
        label_font = QFont("Arial", 10, QFont.Bold)

        # ID Frame
        id_frame = QFrame()
        id_frame.setFrameShape(QFrame.StyledPanel)
        id_layout = QHBoxLayout(id_frame)
        main_layout.addWidget(id_frame)

        # ID Field
        self.customer_id_entry = QLineEdit()
        self.customer_id_entry.setValidator(QIntValidator())
        self.customer_id_entry.setFont(font)
        id_label = QLabel("ID:")
        id_label.setFont(label_font)
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.customer_id_entry)

        # Horizontal Layout for Input Fields (Company Info and Contacts)
        input_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)

        # Frame for Company Info
        company_info_frame = QFrame()
        company_info_frame.setFrameShape(QFrame.StyledPanel)
        company_info_layout = QFormLayout(company_info_frame)
        input_layout.addWidget(company_info_frame)

        # Company Info Title
        company_info_title = QLabel("Company Info")
        company_info_title.setFont(label_font)
        company_info_layout.addRow(company_info_title)

        # Company Info Fields
        self.customer_name_entry = QLineEdit()
        self.customer_address1_entry = QLineEdit()
        self.customer_address2_entry = QLineEdit()
        self.customer_phone_entry = QLineEdit()
        self.customer_emailfax_entry = QLineEdit()

        # Validators for Company Info Fields
        phone_reg_exp = QRegExp("[0-9\-]+")
        self.customer_phone_entry.setValidator(QRegExpValidator(phone_reg_exp))

        # Set Fonts and Add Widgets to Company Info Layout
        for label_text, widget in [
            ("Customer Name:", self.customer_name_entry),
            ("Address:", self.customer_address1_entry),
            ("Address:", self.customer_address2_entry),
            ("Phone #:", self.customer_phone_entry),
            ("Email/Fax:", self.customer_emailfax_entry)
        ]:
            label = QLabel(label_text)
            label.setFont(label_font)
            widget.setFont(font)
            company_info_layout.addRow(label, widget)

        # Frame for Contacts
        contacts_frame = QFrame()
        contacts_frame.setFrameShape(QFrame.StyledPanel)
        contacts_layout = QFormLayout(contacts_frame)
        input_layout.addWidget(contacts_frame)

        # Contacts Title
        contacts_title = QLabel("Contacts")
        contacts_title.setFont(label_font)
        contacts_layout.addRow(contacts_title)

        # Contact Fields
        self.contact_name_entry = QLineEdit()
        self.contact_address1_entry = QLineEdit()
        self.contact_address2_entry = QLineEdit()
        self.contact_phone_entry = QLineEdit()
        self.contact_emailfax_entry = QLineEdit()

        # Validators for Contact Fields
        self.contact_phone_entry.setValidator(QRegExpValidator(phone_reg_exp))

        # Set Fonts and Add Widgets to Contacts Layout
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

        # Button Layout
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        # Buttons
        self.submit_button = QPushButton("Submit")
        self.load_button = QPushButton("Load Customer")
        self.delete_button = QPushButton("Delete Customer")
        self.clear_button = QPushButton("Clear Fields")

        # Apply the custom font to buttons
        self.submit_button.setFont(font)
        self.load_button.setFont(font)
        self.delete_button.setFont(font)
        self.clear_button.setFont(font)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)

        # List Widget for Customer Data
        self.customer_list = QListWidget()
        main_layout.addWidget(self.customer_list)
        self.customer_list.setStyleSheet("alternate-background-color: #505050;")
        self.customer_list.setAlternatingRowColors(True)

        # Set application-wide stylesheet using qdarktheme
        self.setStyleSheet(darktheme_stylesheet)

        self.submit_button.clicked.connect(lambda: self.submit_action(self, conn, c))


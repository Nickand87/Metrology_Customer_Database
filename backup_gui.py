from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QListWidget, QSizePolicy, QFrame, QSplitter
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import qdarktheme


class CustomerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Information")
        self.setGeometry(100, 100, 800, 500)  # Adjusted window size

        # Set style sheets
        dark_stylesheet = qdarktheme.load_stylesheet()

        # Central Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QVBoxLayout(central_widget)
        input_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        listbox_layout = QVBoxLayout()
        status_layout = QHBoxLayout()

        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(listbox_layout)

        # Create a QSplitter for resizable bottom right corner
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Font Settings
        font = QFont("Arial", 14, QFont.Bold)

        # Create widgets
        input_frame = QFrame()
        input_layout.addWidget(input_frame)

        self.customer_id_entry = QLineEdit()
        self.customer_name_entry = QLineEdit()
        self.customer_address1_entry = QLineEdit()
        self.customer_address2_entry = QLineEdit()
        self.customer_phone_entry = QLineEdit()
        self.customer_emailfax_entry = QLineEdit()

        # Apply the custom font to input fields
        self.customer_id_entry.setFont(font)
        self.customer_name_entry.setFont(font)
        self.customer_address1_entry.setFont(font)
        self.customer_address2_entry.setFont(font)
        self.customer_phone_entry.setFont(font)
        self.customer_emailfax_entry.setFont(font)

        input_layout.addWidget(QLabel("ID:"))
        input_layout.addWidget(self.customer_id_entry)
        input_layout.addWidget(QLabel("Customer Name:"))
        input_layout.addWidget(self.customer_name_entry)
        input_layout.addWidget(QLabel("Address Line 1:"))
        input_layout.addWidget(self.customer_address1_entry)
        input_layout.addWidget(QLabel("Address Line 2:"))
        input_layout.addWidget(self.customer_address2_entry)
        input_layout.addWidget(QLabel("Phone #:"))
        input_layout.addWidget(self.customer_phone_entry)
        input_layout.addWidget(QLabel("Email/Fax:"))
        input_layout.addWidget(self.customer_emailfax_entry)

        button_frame = QFrame()
        button_layout.addWidget(button_frame)

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

        listbox_frame = QFrame()
        listbox_layout.addWidget(listbox_frame)

        self.customer_list = QListWidget()

        listbox_layout.addWidget(self.customer_list)

        # Size Grip
        size_grip = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        status_frame = QFrame()
        status_frame.setSizePolicy(size_grip)
        status_layout.addWidget(status_frame)

        # Set application-wide stylesheet using qdarkstyle
        self.setStyleSheet(dark_stylesheet)

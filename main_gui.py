from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QListWidget, QSizePolicy, QFrame, QSplitter
from PyQt5.QtGui import QPalette, QColor, QIcon, QFont
from PyQt5.QtCore import Qt


class CustomerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Information")
        self.setGeometry(100, 100, 800, 500)  # Adjusted window size

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

        # Styling - Larger, modern font, lighter background, bold black text
        primary_color = "#FFFFFF"  # Light gray (almost white)
        secondary_color = "#F2F2F2"  # Lighter gray background
        accent_color = "#333333"  # Bold black

        font = QFont("Arial", 14, QFont.Bold)  # Modern font, larger size, bold

        # Set application-wide stylesheet
        self.setStyleSheet(
            f"background-color: {secondary_color}; color: {accent_color}; border: 2px solid {accent_color}; border-radius: 15px; font-family: 'Arial';")

        # Create widgets
        input_frame = QFrame()
        input_frame.setObjectName("InputFrame")
        input_layout.addWidget(input_frame)

        self.customer_id_entry = QLineEdit()
        self.customer_name_entry = QLineEdit()
        self.customer_address_1_entry = QLineEdit()
        self.customer_address_2_entry = QLineEdit()
        self.customer_phone_entry = QLineEdit()
        self.customer_emailfax_entry = QLineEdit()

        # Apply the custom font to input fields
        self.customer_id_entry.setFont(font)
        self.customer_name_entry.setFont(font)
        self.customer_address_1_entry.setFont(font)
        self.customer_address_2_entry.setFont(font)
        self.customer_phone_entry.setFont(font)
        self.customer_emailfax_entry.setFont(font)

        input_layout.addWidget(QLabel("ID:"))
        input_layout.addWidget(self.customer_id_entry)
        input_layout.addWidget(QLabel("Customer Name:"))
        input_layout.addWidget(self.customer_name_entry)
        input_layout.addWidget(QLabel("Address Line 1:"))
        input_layout.addWidget(self.customer_address_1_entry)
        input_layout.addWidget(QLabel("Address Line 2:"))
        input_layout.addWidget(self.customer_address_2_entry)
        input_layout.addWidget(QLabel("Phone #:"))
        input_layout.addWidget(self.customer_phone_entry)
        input_layout.addWidget(QLabel("Email/Fax:"))
        input_layout.addWidget(self.customer_emailfax_entry)

        button_frame = QFrame()
        button_frame.setObjectName("ButtonFrame")
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

        # Apply button styles
        button_style = f"background-color: {accent_color}; color: {primary_color}; border: 2px solid {accent_color}; border-radius: 10px;"
        self.submit_button.setStyleSheet(button_style)
        self.load_button.setStyleSheet(button_style)
        self.delete_button.setStyleSheet(button_style)
        self.clear_button.setStyleSheet(button_style)

        listbox_frame = QFrame()
        listbox_frame.setObjectName("ListBoxFrame")
        listbox_layout.addWidget(listbox_frame)

        self.customer_list = QListWidget()
        self.customer_list.setStyleSheet(
            f"background-color: {primary_color}; color: {accent_color}; font: 14pt Arial; border: 2px solid {accent_color}; border-radius: 15px;")

        listbox_layout.addWidget(self.customer_list)

        # Size Grip
        size_grip = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        status_frame = QFrame()
        status_frame.setSizePolicy(size_grip)
        status_layout.addWidget(status_frame)

        # Set custom palette
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(accent_color))
        palette.setColor(QPalette.Window, QColor(primary_color))
        palette.setColor(QPalette.Button, QColor(accent_color))
        self.setPalette(palette)

        # Set window icon (replace 'icon.png' with your icon file)
        self.setWindowIcon(QIcon('icon.png'))
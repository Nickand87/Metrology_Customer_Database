from client_window import ClientWindow
from main_gui import CustomerApp
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QMessageBox
import sqlite3
import os
import sys


class MainWindow(QMainWindow):
    def __init__(self, conn, c):
        super().__init__()

        self.setWindowTitle("Dynamic UI Application")
        self.setGeometry(100, 100, 800, 600)

        # Main horizontal layout
        main_layout = QHBoxLayout()

        # Sidebar layout for buttons
        sidebar_layout = QVBoxLayout()

        # Buttons for the sidebar
        self.button1 = QPushButton("Clients")
        self.button1.clicked.connect(lambda: self.switch_page(0))
        sidebar_layout.addWidget(self.button1)

        self.button2 = QPushButton("Settings")
        self.button2.clicked.connect(lambda: self.switch_page(1))
        sidebar_layout.addWidget(self.button2)

        # Add stretch to push all buttons to the top
        sidebar_layout.addStretch()

        # Stacked widget for dynamic content
        self.stacked_widget = QStackedWidget()

        # Adding pages to the stacked widget
        self.page1 = ClientWindow(conn, c) # Assuming Page1 is a QWidget subclass defined in another file
        self.page2 = CustomerApp() # Assuming Page2 is a QWidget subclass defined in another file

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

        # Add sidebar and stacked widget to the main layout
        main_layout.addLayout(sidebar_layout, 1) # Sidebar with a smaller stretch factor
        main_layout.addWidget(self.stacked_widget, 4) # Content area with a larger stretch factor

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def switch_page(self, page_index):
        self.stacked_widget.setCurrentIndex(page_index)


# Assuming Page1 and Page2 are defined like this
class Page1(QWidget):
    def __init__(self):
        super().__init__()
        # Define the UI for Page1 here


class Page2(QWidget):
    def __init__(self):
        super().__init__()
        # Define the UI for Page2 here


def read_db_path_from_settings():
    try:
        with open("settings.txt", "r") as file:
            return file.readline().strip()
    except FileNotFoundError:
        QMessageBox.critical(None, "Error", "Settings file not found.")
        exit()


def main():
    app = QApplication(sys.argv)

    db_directory = read_db_path_from_settings()
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
    db_path = os.path.join(db_directory, "customer_info.db")

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS customers 
                                (id INTEGER PRIMARY KEY, customer_id INTEGER, customer_name TEXT, customer_address_1 TEXT, customer_address_2 TEXT, customer_phone TEXT, customer_emailfax TEXT)''')

    except Exception as e:
        print(f"Error: {str(e)}")

    mainWin = MainWindow(conn, c)
    mainWin.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
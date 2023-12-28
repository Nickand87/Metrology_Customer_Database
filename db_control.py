import sqlite3
from PyQt5.QtWidgets import QMessageBox
import sys


class DatabaseManager:
    """Handles database operations."""
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.initialize_database()

    def initialize_database(self):
        """Initialize the database schema."""
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS customers 
                                   (id INTEGER PRIMARY KEY, customer_id INTEGER, customer_name TEXT, 
                                    customer_address_1 TEXT, customer_address_2 TEXT, 
                                    customer_phone TEXT, customer_emailfax TEXT)''')
        except sqlite3.Error as e:
            print(f"Database Error: {str(e)}")
            QMessageBox.critical(None, "Database Error", str(e))
            sys.exit(1)

    # Add other database-related methods here if needed
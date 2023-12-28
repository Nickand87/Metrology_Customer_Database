import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QSizePolicy, QFrame, QMessageBox
from backup_gui import CustomerApp
import sqlite3
import os
import random


def load_customer(app, c):
    selected_item = app.customer_list.selectedItems()
    if selected_item:
        customer_id = selected_item[0].text().split(':')[0]
        c.execute("SELECT * FROM customers WHERE customer_id=?", (customer_id,))
        customer = c.fetchone()
        if customer:
            clear_entries(app)
            app.customer_id_entry.setReadOnly(False)
            app.customer_id_entry.setText(customer_id)
            app.customer_id_entry.setReadOnly(True)
            app.customer_name_entry.setText(customer[2])
            app.customer_address1_entry.setText(customer[3])
            app.customer_address2_entry.setText(customer[4])
            app.customer_phone_entry.setText(customer[5])
            app.customer_emailfax_entry.setText(customer[6])
        else:
            QMessageBox.critical(app, "Error", "Customer not found")
    else:
        QMessageBox.critical(app, "Error", "No customer selected")
    view_customers(app, c)


def read_db_path_from_settings():
    try:
        with open("settings.xml", "r") as file:
            return file.readline().strip()
    except FileNotFoundError:
        QMessageBox.critical(None, "Error", "Settings file not found.")
        exit()


def submit_action(app, conn, c):
    customer_id = app.customer_id_entry.text()
    customer_name = app.customer_name_entry.text()
    customer_address1 = app.customer_address1_entry.text()
    customer_address2 = app.customer_address2_entry.text()
    customer_phone = app.customer_phone_entry.text()
    customer_email_fax = app.customer_emailfax_entry.text()

    if customer_id:
        c.execute("UPDATE customers SET customer_name=?, customer_address1=?, customer_address2=?, customer_emailfax=?, customer_phone=? WHERE customer_id=?",
                  (customer_name, customer_address1, customer_address2, customer_email_fax, customer_phone, customer_id))
    else:
        while True:
            new_id = random.randint(100000, 999999)
            c.execute("SELECT customer_id FROM customers WHERE customer_id=?", (new_id,))
            if not c.fetchone():
                break

        c.execute("INSERT INTO customers (customer_id, customer_name, customer_address1, customer_address2, customer_emailfax, customer_phone) VALUES (?, ?, ?, ?, ?, ?)",
                  (new_id, customer_name, customer_address1, customer_address2, customer_email_fax, customer_phone))

    conn.commit()
    QMessageBox.information(app, "Submitted", f"Information Submitted for {customer_name}")
    view_customers(app, c)


def view_customers(app, c):
    c.execute("SELECT customer_id, customer_name, customer_address1 FROM customers")
    all_customers = c.fetchall()
    app.customer_list.clear()
    for customer in all_customers:
        app.customer_list.addItem(f"{customer[0]}: {customer[1]}: {customer[2]}")


def delete_customer(app, c, conn):
    selected_item = app.customer_list.selectedItems()
    if selected_item:
        customer_id = selected_item[0].text().split(':')[0]
        c.execute("DELETE FROM customers WHERE customer_id=?", (customer_id,))
        conn.commit()
        view_customers(app, c)
        clear_entries(app)
    else:
        QMessageBox.critical(app, "Error", "No customer selected")


def clear_entries(app):
    app.customer_id_entry.setReadOnly(False)
    app.customer_id_entry.clear()
    app.customer_id_entry.setReadOnly(True)
    app.customer_name_entry.clear()
    app.customer_address1_entry.clear()
    app.customer_address2_entry.clear()
    app.customer_phone_entry.clear()
    app.customer_emailfax_entry.clear()


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
                        (id INTEGER PRIMARY KEY, customer_id INTEGER, customer_name TEXT, customer_address1 TEXT, customer_address2 TEXT, customer_phone TEXT, customer_emailfax TEXT)''')

        window = CustomerApp()
        window.show()

        window.submit_button.clicked.connect(lambda: submit_action(window, conn, c))
        window.clear_button.clicked.connect(lambda: clear_entries(window))
        window.load_button.clicked.connect(lambda: load_customer(window, c))
        window.delete_button.clicked.connect(lambda: delete_customer(window, c, conn))
        window.customer_list.itemDoubleClicked.connect(lambda item: load_customer(window, c))

        view_customers(window, c)

        sys.exit(app.exec())
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
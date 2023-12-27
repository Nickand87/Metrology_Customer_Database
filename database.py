from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QSizePolicy, QFrame, QMessageBox
import sqlite3
import os

def read_db_path_from_settings():
    try:
        with open("settings.txt", "r") as file:
            return file.readline().strip()
    except FileNotFoundError:
        QMessageBox.critical(None, "Error", "Settings file not found.")
        exit()

def initialize_database():



import sys
import os
import csv
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QIcon, QMovie
from AccountRegistration import RegistrationApp
from MainChatroom import Main_Chatroom
from database import create_tables,get_user,get_all_users


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Menu & Login Screen"
        self.x = 200 # or Left
        self.y = 200 # or Top
        self.width = 350
        self.height = 450
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.createGridLayout()
        self.setLayout(self.layout)
        self.show()

    def createGridLayout(self):
        self.layout = QGridLayout()
        self.layout.setColumnStretch(1, 2)

        # GIF Display
        self.gif_label = QLabel(self)
        self.movie = QMovie("/Users/lourdes/Desktop/TIP.png")
        self.movie.setScaledSize(QtCore.QSize(250, 150))
        self.gif_label.setMovie(self.movie)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.movie.start()

        # Widgets
        self.textboxlbl = QLabel("Username: ", self)
        self.textbox = QLineEdit(self)
        
        self.passwordlbl = QLabel("Password: ", self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.login_button = QPushButton('Login', self)
        self.login_button.setToolTip("Click to log in")
        self.login_button.clicked.connect(self.handle_login)

        self.register_button = QPushButton('Register Account', self)
        self.register_button.setToolTip("Click to open registration form")
        self.register_button.clicked.connect(self.open_registration)

        # Layout placements
        self.layout.addWidget(self.gif_label, 0, 1, 1, 2)
        self.layout.addWidget(self.textboxlbl, 1, 1)
        self.layout.addWidget(self.textbox, 1, 2)
        self.layout.addWidget(self.passwordlbl, 2, 1)
        self.layout.addWidget(self.password, 2, 2)
        self.layout.addWidget(self.login_button, 3, 2)
        self.layout.addWidget(self.register_button, 4, 2)

    def handle_login(self):
        username = self.textbox.text().strip()
        password = self.password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both username and password.")
            return

        users = get_all_users()
        if not users:
            QMessageBox.critical(self, "Error", "No registered accounts found. Please register first.")
            return
        
        user = get_user(username)

        if user and user[2] == password:
            QMessageBox.information(self, "Menu Interface", f"Login Successful!\nWelcome to the Menu, {username}!")
            self.textbox.clear()
            self.password.clear()

            self.chat_window = Main_Chatroom(user_id=user[0],username=username)
            self.chat_window.show()

            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_registration(self):
        self.reg_window = RegistrationApp()
        self.reg_window.show()

if __name__ == '__main__':
    create_tables()

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())

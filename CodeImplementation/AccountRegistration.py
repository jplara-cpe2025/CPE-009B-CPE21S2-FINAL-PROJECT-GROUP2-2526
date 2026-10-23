import sys
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtGui import QMovie

from database import create_user

class RegistrationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Account Registration"
        self.x = 200
        self.y = 200
        self.width = 400
        self.height = 550
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height)
        
        # Color Palette Stylesheet
        self.setStyleSheet("""
            QWidget { background-color: #F8FAFC; color: #1E1B4B; font-family: 'Segoe UI', sans-serif; }
            QLabel { font-size: 12px; font-weight: 600; color: #1E1B4B; }
            QLineEdit { background-color: #FFFFFF; color: #1E1B4B; border: 1px solid #CBD5E1; border-radius: 6px; padding: 6px 10px; font-size: 13px; min-width: 220px;}
            QLineEdit:focus { border: 2px solid #8B5CF6; }
            QPushButton { background-color: #8B5CF6; color: #FFFFFF; border: none; border-radius: 6px; padding: 8px; font-weight: bold; font-size: 13px; }
            QPushButton:hover { background-color: #7C3AED; }
        """)

        self.createGridLayout()
        self.setLayout(self.layout)
        self.show()

    def createGridLayout(self):
        self.layout = QGridLayout()
        self.layout.setColumnStretch(1, 2)

        # GIF Display
        self.gif_label = QLabel(self)
        try:
            self.movie = QMovie("TIP.jpg")
            self.movie.setScaledSize(QtCore.QSize(200, 200)) 
            self.gif_label.setMovie(self.movie)
            self.movie.start()
        except Exception:
            self.gif_label.setText("📝 Account Registration")
            self.gif_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #8B5CF6;")
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        # Input Widgets
        self.first_namelbl = QLabel("First Name: ", self)
        self.first_name = QLineEdit(self)

        self.last_namelbl = QLabel("Last Name: ", self)
        self.last_name = QLineEdit(self)

        self.emaillbl = QLabel("Email Address: ", self)
        self.email = QLineEdit(self)

        self.contactlbl = QLabel("Contact Number: ", self)
        self.contact = QLineEdit(self)

        self.textboxlbl = QLabel("Username: ", self)
        self.textbox = QLineEdit(self)

        self.passwordlbl = QLabel("Password: ", self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.button = QPushButton('Register', self)
        self.button.setToolTip("Click to register your account")
        self.button.clicked.connect(self.register_account)

        # Layout
        self.layout.addWidget(self.gif_label, 0, 1, 1, 2)
        self.layout.addWidget(self.first_namelbl, 1, 1)
        self.layout.addWidget(self.first_name, 1, 2)
        self.layout.addWidget(self.last_namelbl, 2, 1)
        self.layout.addWidget(self.last_name, 2, 2)
        self.layout.addWidget(self.emaillbl, 3, 1)
        self.layout.addWidget(self.email, 3, 2)
        self.layout.addWidget(self.contactlbl, 4, 1)
        self.layout.addWidget(self.contact, 4, 2)
        self.layout.addWidget(self.textboxlbl, 5, 1)
        self.layout.addWidget(self.textbox, 5, 2)
        self.layout.addWidget(self.passwordlbl, 6, 1)
        self.layout.addWidget(self.password, 6, 2)
        self.layout.addWidget(self.button, 7, 2)

    def register_account(self):
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        email = self.email.text().strip()
        contact = self.contact.text().strip()
        username = self.textbox.text().strip()
        password = self.password.text().strip()

        # Check for empty fields
        if not all([first_name, last_name, email, contact, username, password]):
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Registration Error")
            msg_box.setText("Please fill in all fields before registering.")
            msg_box.exec()
            return

        # Save the account to the database
        success, msg = create_user(username, password)

        if success:
            # Success Notification
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Registration Successful")
            msg_box.setText(f"Account for '{username}' registered successfully!")
            msg_box.exec()

            # Clear inputs
            self.first_name.clear()
            self.last_name.clear()
            self.email.clear()
            self.contact.clear()
            self.textbox.clear()
            self.password.clear()
            self.close()
        else:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Registration Error")
            msg_box.setText(msg)
            msg_box.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegistrationApp()
    sys.exit(app.exec())
    
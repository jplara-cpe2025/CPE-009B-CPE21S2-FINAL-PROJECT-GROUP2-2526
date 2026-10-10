import sys
import os
import csv
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtGui import QIcon, QMovie

CSV_FILE = "Accounts.csv"

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
        
        self.createGridLayout()
        self.setLayout(self.layout)
        self.show()

    def createGridLayout(self):
        self.layout = QGridLayout()
        self.layout.setColumnStretch(1, 2)

        # GIF Display
        self.gif_label = QLabel(self)
        self.movie = QMovie("/Users/lourdes/Desktop/TIP.png")
        self.movie.setScaledSize(QtCore.QSize(300, 400)) 
        self.gif_label.setMovie(self.movie)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.movie.start()

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

        # Save the account to a CSV file
        try:
            file_exists = os.path.isfile(CSV_FILE)

            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Writing of header file if the file does not exist
                if not file_exists:
                    writer.writerow(['First Name', 'Last Name', 'Email', 'Contact Number', 'Username', 'Password'])
                
                writer.writerow([first_name, last_name, email, contact, username, password])

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

        except Exception as e:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("File Error")
            msg_box.setText(f"An error occurred while saving to CSV: {str(e)}")
            msg_box.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegistrationApp()
    sys.exit(app.exec())        title_label.move(110, 15)

        # GIF Integration
        gif_path = os.path.join(script_dir, "200w.gif")
        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(160, 50, 100, 100)

        # Ensure the file exists before attempting to load
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            self.gif_label.setMovie(self.movie)
            self.gif_label.setScaledContents(True)
            self.movie.start()
        else:
            self.gif_label.setText("GIF Not Found")

        # Form Absolute Positioning
        top_start = 165
        row_height = 35
        label_x = 40
        field_x = 160
        field_width = 200
        field_height = 25

        fields = [
            ("First Name:", "txt_first_name", False),
            ("Last Name:", "txt_last_name", False),
            ("Username:", "txt_username", False),
            ("Password:", "txt_password", True),
            ("Email Address:", "txt_email", False),
            ("Contact Number:", "txt_contact", False),
        ]

        self.inputs = {}
        for idx, (label_text, field_name, is_password) in enumerate(fields):
            current_y = top_start + (idx * row_height)
            lbl = QLabel(label_text, self)
            lbl.move(label_x, current_y + 3)

            txt = QLineEdit(self)
            txt.setGeometry(field_x, current_y, field_width, field_height)
            if is_password:
                txt.setEchoMode(QLineEdit.EchoMode.Password)

            self.inputs[field_name] = txt

        buttons_y = top_start + (len(fields) * row_height) + 15

        self.btn_submit = QPushButton("Submit", self)
        self.btn_submit.setGeometry(80, buttons_y, 110, 32)
        self.btn_submit.clicked.connect(self.submit_form)

        self.btn_clear = QPushButton("Clear", self)
        self.btn_clear.setGeometry(220, buttons_y, 110, 32)
        self.btn_clear.clicked.connect(self.clear_form)

    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.width) // 2
        y = (screen.height() - self.height) // 2
        self.move(x, y)

    def submit_form(self):
        first_name = self.inputs["txt_first_name"].text()
        if not first_name:
            QMessageBox.warning(self, "Warning", "Please fill in required fields!")
        else:
            QMessageBox.information(
                self, "Success", "Account registered successfully!"
            )

    def clear_form(self):
        for txt in self.inputs.values():
            txt.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec())

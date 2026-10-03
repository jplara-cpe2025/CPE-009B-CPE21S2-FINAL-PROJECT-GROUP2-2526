import sys
import os
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QApplication,
)
from PyQt6.QtGui import QIcon, QFont, QGuiApplication, QMovie


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Account Registration System"
        self.width = 420
        self.height = 460
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        # Base path for relative resources
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "pythonico.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.resize(self.width, self.height)
        self.center_window()

        # Program Title
        title_label = QLabel("Account Registration", self)
        title_font = QFont("Arial", 14)
        title_font.setWeight(QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.move(110, 15)

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
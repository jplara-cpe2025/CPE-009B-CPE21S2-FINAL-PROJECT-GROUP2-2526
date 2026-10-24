import sys
from PyQt6.QtCore import Qt, QByteArray, QSize
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtSvg import QSvgRenderer

from database import create_user

BG_COLOR = "#F5F5DC"
INK_COLOR = "#000000"
BTN_COLOR = "#57534B"
BTN_HOVER = "#3F3C36"
BTN_TEXT = "#F5F5DC"

def _svg(body, color=INK_COLOR):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
            f'fill="{color}" stroke="none">{body}</svg>')

ICON_USER = _svg('<circle cx="12" cy="7.5" r="5"/><path d="M2.5 22c0-5.5 4.2-8.5 9.5-8.5s9.5 3 9.5 8.5z"/>')

ICON_EMAIL = _svg(
    '<g fill="none" stroke="#000" stroke-width="1.8" stroke-linejoin="round">'
    '<rect x="2.5" y="4.5" width="19" height="15" rx="2"/>'
    '<path d="M3 5.5l9 7.5 9-7.5M3 19l6.5-7M21 19l-6.5-7"/></g>')

ICON_PHONE = _svg(
    '<path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 '
    '1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 '
    '0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>')

ICON_USERNAME = _svg(
    '<g fill="none" stroke="#000" stroke-width="1.8" stroke-linecap="round">'
    '<rect x="2.5" y="4" width="19" height="16" rx="3"/>'
    '<circle cx="8.5" cy="10" r="2"/><path d="M5.5 16c.5-2 2-2.8 3-2.8s2.5.8 3 2.8"/>'
    '<path d="M14.5 10h4M14.5 14h4"/></g>')

ICON_LOCK = _svg(
    '<path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12'
    'c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9'
    'H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>')

APP_ICON_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    f'<rect width="64" height="64" rx="14" fill="{BTN_COLOR}"/>'
    f'<g fill="{BG_COLOR}"><circle cx="26" cy="22" r="9"/>'
    '<path d="M8 50c0-10 8-15 18-15s18 5 18 15z"/>'
    f'<path d="M47 12h4v8h8v4h-8v8h-4v-8h-8v-4h8z" transform="translate(-6 -2)"/></g></svg>'
)


def svg_to_pixmap(svg_text, size):
    renderer = QSvgRenderer(QByteArray(svg_text.encode("utf-8")))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


def make_app_icon():
    icon = QIcon()
    for s in (16, 32, 48, 64, 128, 256):
        icon.addPixmap(svg_to_pixmap(APP_ICON_SVG, s))
    return icon


class RegistrationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Account Registration"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(make_app_icon())
        self.setGeometry(200, 200, 560, 420)
        self.setMinimumSize(480, 380)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {INK_COLOR};
                font-family: 'Segoe UI', sans-serif;
            }}
            QLabel {{ font-size: 16px; background: transparent; }}
            QLineEdit {{
                background-color: transparent;
                color: {INK_COLOR};
                border: 2px solid {INK_COLOR};
                border-radius: 19px;
                padding: 0 14px;
                font-size: 14px;
                min-width: 220px;
                min-height: 36px;
            }}
            QLineEdit:focus {{ background-color: #FFFFFF; }}
            QPushButton {{
                background-color: {BTN_COLOR};
                color: {BTN_TEXT};
                border: 2px solid {INK_COLOR};
                border-radius: 19px;
                min-height: 36px;
                font-size: 13px;
            }}
            QPushButton:hover {{ background-color: {BTN_HOVER}; }}
            QPushButton:pressed {{ background-color: {INK_COLOR}; }}
        """)

        self.createGridLayout()
        self.setLayout(self.layout)
        self.show()

    def make_label(self, text, svg):
        """Text label followed by an icon, like in the mockup."""
        container = QWidget(self)
        row = QHBoxLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)

        text_lbl = QLabel(text, container)
        icon_lbl = QLabel(container)
        icon_lbl.setPixmap(svg_to_pixmap(svg, 24))
        icon_lbl.setFixedSize(QSize(24, 24))

        row.addWidget(text_lbl)
        row.addWidget(icon_lbl)
        row.addStretch()
        return container

    def createGridLayout(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setVerticalSpacing(14)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

        # Input widgets
        self.first_name = QLineEdit(self)
        self.last_name = QLineEdit(self)
        self.email = QLineEdit(self)
        self.contact = QLineEdit(self)
        self.textbox = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.button = QPushButton("Register", self)
        self.button.setToolTip("Click to register your account")
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.clicked.connect(self.register_account)

        rows = [
            ("First Name:", ICON_USER, self.first_name),
            ("Last Name:", ICON_USER, self.last_name),
            ("Email:", ICON_EMAIL, self.email),
            ("Contact Number:", ICON_PHONE, self.contact),
            ("Username:", ICON_USERNAME, self.textbox),
            ("Password:", ICON_LOCK, self.password),
        ]
        for i, (text, svg, field) in enumerate(rows):
            self.layout.addWidget(self.make_label(text, svg), i, 0)
            self.layout.addWidget(field, i, 1)

        self.layout.setRowMinimumHeight(len(rows), 10)
        self.layout.addWidget(self.button, len(rows) + 1, 1)

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
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("registration.app.1")
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setWindowIcon(make_app_icon())
    ex = RegistrationApp()

    sys.exit(app.exec())

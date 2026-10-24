import sys
from PyQt6.QtCore import Qt, QByteArray, QSize, QRectF, QPointF, QPropertyAnimation, QPoint
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QIcon, QColor, QFont
from PyQt6.QtSvg import QSvgRenderer

from AccountRegistration import RegistrationApp
from database import create_tables, get_user, get_all_users

BG_COLOR = "#F5F5DC"
INK_COLOR = "#000000"
BTN_COLOR = "#57534B"
BTN_HOVER = "#3F3C36"
BTN_TEXT = "#F5F5DC"
LOGO_BUBBLE = "#D5D1BB"
FACE_FILL = "#E8CBAE"
FACE_LINE = "#4A2A1A"

ICON_USERNAME = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<g fill="none" stroke="#000" stroke-width="1.8" stroke-linecap="round">'
    '<rect x="2.5" y="4" width="19" height="16" rx="3"/>'
    '<circle cx="8.5" cy="10" r="2"/><path d="M5.5 16c.5-2 2-2.8 3-2.8s2.5.8 3 2.8"/>'
    '<path d="M14.5 10h4M14.5 14h4"/></g></svg>'
)

ICON_LOCK = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#000">'
    '<path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12'
    'c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9'
    'H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>'
)

FACE_BODY = (
    f'<path d="M24 5C12 5 3 12 3 22c0 5 2.5 9 6.5 12L6 43l9-5c3 1.2 5.5 1.5 9 1.5 '
    f'12 0 21-7 21-17.5S36 5 24 5z" fill="{FACE_FILL}" stroke="{FACE_LINE}" '
    f'stroke-width="2.4" stroke-linejoin="round"/>'
    f'<path d="M12 21q4-3.5 8 0M28 21q4-3.5 8 0" fill="none" stroke="{FACE_LINE}" '
    f'stroke-width="1.8" stroke-linecap="round"/>'
)

FACE_SVG = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">{FACE_BODY}</svg>'

APP_ICON_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    f'<rect width="64" height="64" rx="14" fill="{LOGO_BUBBLE}"/>'
    f'<g transform="translate(8 8)">{FACE_BODY}</g></svg>'
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


class LogoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(262, 134)
        self.face = QSvgRenderer(QByteArray(FACE_SVG.encode("utf-8")))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bubble = QPainterPath()
        bubble.addRoundedRect(QRectF(4, 4, 254, 97), 30, 30)

        tail = QPainterPath()
        tail.moveTo(QPointF(74, 96))
        tail.lineTo(QPointF(64, 128))
        tail.lineTo(QPointF(112, 96))
        tail.closeSubpath()

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(LOGO_BUBBLE))
        painter.drawPath(bubble.united(tail))

        self.face.render(painter, QRectF(24, 26, 48, 48))

        font = QFont("Segoe UI")
        font.setPixelSize(38)
        painter.setFont(font)
        painter.setPen(QColor(INK_COLOR))
        painter.drawText(QRectF(82, 4, 170, 97), int(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft), "DChat")
        painter.end()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Menu & Login Screen"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(make_app_icon())
        self.setGeometry(200, 200, 560, 400)
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
                min-width: 200px;
                min-height: 34px;
            }}
            QLineEdit:focus {{ background-color: #FFFFFF; }}
            QPushButton#loginBtn, QPushButton#regBtn {{
                background-color: {BTN_COLOR};
                color: {BTN_TEXT};
                border: 2px solid {INK_COLOR};
                border-radius: 19px;
                min-height: 34px;
                font-size: 13px;
            }}
            QPushButton#loginBtn:hover, QPushButton#regBtn:hover {{ background-color: {BTN_HOVER}; }}
            QPushButton#loginBtn:pressed, QPushButton#regBtn:pressed {{ background-color: {INK_COLOR}; }}
        """)

        self.createGridLayout()
        self.setLayout(self.layout)
        self.show()

    def make_label(self, text, svg):
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
        self.layout.setContentsMargins(28, 16, 28, 24)
        self.layout.setVerticalSpacing(12)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

        self.logo = LogoWidget(self)

        self.textbox = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.textbox.returnPressed.connect(self.password.setFocus)
        self.password.returnPressed.connect(self.handle_login)

        self.login_button = QPushButton('Log In', self)
        self.login_button.setObjectName("loginBtn")
        self.login_button.setToolTip("Click to log in")
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)

        self.register_button = QPushButton('Register', self)
        self.register_button.setObjectName("regBtn")
        self.register_button.setToolTip("Click to open registration form")
        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_button.clicked.connect(self.open_registration)

        self.layout.addWidget(self.logo, 0, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        self.layout.setRowMinimumHeight(1, 16)
        self.layout.addWidget(self.make_label("Username:", ICON_USERNAME), 2, 0)
        self.layout.addWidget(self.textbox, 2, 1)
        self.layout.addWidget(self.make_label("Password:", ICON_LOCK), 3, 0)
        self.layout.addWidget(self.password, 3, 1)
        self.layout.addWidget(self.login_button, 4, 1)
        self.layout.addWidget(self.register_button, 5, 1)
        self.layout.setRowStretch(6, 1)

    def handle_login(self):
        username = self.textbox.text().strip()
        password = self.password.text().strip()

        if not username or not password:
            self.shake()
            QMessageBox.warning(self, "Login Error", "Please enter both username and password.")
            return

        users = get_all_users()
        if not users:
            self.shake()
            QMessageBox.critical(self, "Error", "No registered accounts found. Please register first.")
            return

        user = get_user(username, password)

        if user and user[2] == password:
            self.shake()
            QMessageBox.information(self, "Menu Interface", f"Login Successful!\nWelcome to the Menu, {username}!")
            self.textbox.clear()
            self.password.clear()

            self.open_chatroom(user, username)
            self.close()

        else:
            self.shake()
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_registration(self):
        self.reg_window = RegistrationApp()
        self.reg_window.show()

    def open_chatroom(self, user, username):
        from MainChatroom import Main_Chatroom
        self.chat_window = Main_Chatroom(user_id=user[0], username=username)
        self.chat_window.show()

    def shake(self):
        if hasattr(self, "shake_anim") and self.shake_anim.state() == QPropertyAnimation.State.Running:
            return

        current_pos = self.pos()
        self.shake_anim = QPropertyAnimation(self, b"pos")
        self.shake_anim.setDuration(300)

        self.shake_anim.setKeyValueAt(0.00, current_pos)
        self.shake_anim.setKeyValueAt(0.20, current_pos + QPoint(-12, 0))
        self.shake_anim.setKeyValueAt(0.40, current_pos + QPoint(12, 0))
        self.shake_anim.setKeyValueAt(0.60, current_pos + QPoint(-8, 0))
        self.shake_anim.setKeyValueAt(0.80, current_pos + QPoint(8, 0))
        self.shake_anim.setKeyValueAt(1.00, current_pos)

        self.shake_anim.start()


if __name__ == '__main__':
    create_tables()

    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("dchat.app.1")
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setWindowIcon(make_app_icon())
    ex = App()
    sys.exit(app.exec())

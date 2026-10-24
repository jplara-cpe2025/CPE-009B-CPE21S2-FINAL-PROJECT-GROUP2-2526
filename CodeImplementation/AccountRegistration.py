import sys
import os
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QMainWindow, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QDialog, QFileDialog)
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QIcon

from database import (save_message, get_all_users, get_messages, 
                      update_user_avatar, update_username, get_user_by_id)

from MenuInterface import App
# Helper function to crop and render smooth circular pixmaps for avatars
def get_circular_pixmap(image_path, size=28):
    if image_path and os.path.exists(image_path):
        src_pixmap = QPixmap(image_path)
        if not src_pixmap.isNull():
            scaled = src_pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            out_pixmap = QPixmap(size, size)
            out_pixmap.fill(Qt.GlobalColor.transparent)

            painter = QPainter(out_pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, size, size)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, scaled)
            painter.end()
            return out_pixmap
    return None

# Profile Edit Dialog
class ProfileDialog(QDialog):
    def __init__(self, user_id, current_username, current_avatar, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.current_username = current_username
        self.current_avatar = current_avatar
        self.new_avatar_path = current_avatar

        self.setWindowTitle("Edit Profile")
        self.setFixedSize(320, 320)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        # Centered Avatar Preview
        self.avatar_preview = QLabel()
        self.avatar_preview.setFixedSize(64, 64)
        self.avatar_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_avatar_preview(self.current_avatar)

        avatar_container = QHBoxLayout()
        avatar_container.addStretch()
        avatar_container.addWidget(self.avatar_preview)
        avatar_container.addStretch()
        layout.addLayout(avatar_container)
        layout.addSpacing(25)

        # Change Avatar Button
        change_avatar_btn = QPushButton("Change Avatar")
        change_avatar_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #2563EB; }
        """)
        change_avatar_btn.clicked.connect(self.select_new_avatar)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(change_avatar_btn)
        btn_container.addStretch()
        layout.addLayout(btn_container)

        # Username Input
        user_label = QLabel("Username")
        user_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #1E1B4B; margin-top: 4px;")
        layout.addWidget(user_label)

        self.username_input = QLineEdit(self.current_username)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 8px 10px;
                font-size: 13px;
                color: #1E1B4B;
            }
        """)
        layout.addWidget(self.username_input)

        layout.addStretch()

        # Save Button
        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B5CF6;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 9px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #7C3AED; }
        """)
        save_btn.clicked.connect(self.save_profile)
        layout.addWidget(save_btn)

        # Logout Button
        logout_btn = QPushButton("Log Out")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B5CF6;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 9px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #7C3AED; }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

    def update_avatar_preview(self, path):
        pix = get_circular_pixmap(path, size=64)
        if pix:
            self.avatar_preview.setPixmap(pix)
            self.avatar_preview.setStyleSheet("border: none; background: transparent;")
        else:
            initial = self.current_username[0].upper() if self.current_username else "U"
            self.avatar_preview.setText(initial)
            self.avatar_preview.setStyleSheet("""
                background-color: #3B82F6;
                color: #FFFFFF;
                border-radius: 32px;
                font-size: 24px;
                font-weight: bold;
            """)

    def select_new_avatar(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Avatar Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.new_avatar_path = file_path
            self.update_avatar_preview(file_path)

    def save_profile(self):
        new_name = self.username_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Error", "Username cannot be empty.")
            return

        if new_name != self.current_username:
            success, msg = update_username(self.user_id, new_name)
            if not success:
                QMessageBox.warning(self, "Error", msg)
                return

        if self.new_avatar_path != self.current_avatar:
            update_user_avatar(self.user_id, self.new_avatar_path)

        QMessageBox.information(self, "Success", "Profile updated successfully!")
        self.accept()

    def logout(self):
        reply = QMessageBox.warning(self,"Log Out","Are you sure you want to log out?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            self.parent().logout()
        else:
            self.close

# Popup Emoji Selector Widget
class EmojiPicker(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Emoji")
        self.setFixedSize(220, 180)
        self.selected_emoji = ""

        grid = QGridLayout()
        emojis = [
            '😊', '😂', '👍', '❤️', '🎉',
            '🔥', '😎', '🙏', '😭', '✨',
            '👋', '🤔', '💯', '🚀', '🥳'
        ]

        positions = [(i, j) for i in range(3) for j in range(5)]
        for pos, emoji in zip(positions, emojis):
            btn = QPushButton(emoji)
            btn.setFixedSize(36, 36)
            btn.setStyleSheet("font-size: 16px; border: 1px solid #CBD5E1; border-radius: 6px; background: #FFFFFF; color: #1E1B4B;")
            btn.clicked.connect(lambda _, e=emoji: self.pick_emoji(e))
            grid.addWidget(btn, *pos)

        self.setLayout(grid)

    def pick_emoji(self, emoji):
        self.selected_emoji = emoji
        self.accept()


# Custom Widget for Contacts Sidebar List with Avatar
class ContactItemWidget(QWidget):
    def __init__(self, username, avatar_path):
        super().__init__()
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(10)

        avatar_label = QLabel()
        avatar_label.setFixedSize(28, 28)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        circular_pix = get_circular_pixmap(avatar_path, size=28)
        if circular_pix:
            avatar_label.setPixmap(circular_pix)
        else:
            initial = username[0].upper() if username else "U"
            avatar_label.setText(initial)
            avatar_label.setStyleSheet("""
                background-color: #3B82F6;
                color: #FFFFFF;
                border-radius: 14px;
                font-size: 12px;
                font-weight: bold;
            """)

        name_label = QLabel(username)
        name_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #1E1B4B; background: transparent;")

        layout.addWidget(avatar_label)
        layout.addWidget(name_label)
        layout.addStretch()


# Custom Widget for Message Bubbles (hehe Tried to do it like old messenger)
class MessageBubble(QWidget):
    def __init__(self, message, timestamp, is_self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)
        main_layout.setSpacing(2)

        container = QWidget()
        box_layout = QVBoxLayout(container)
        box_layout.setContentsMargins(12, 8, 12, 8)

        msg_label = QLabel(message)
        msg_label.setWordWrap(True)

        time_label = QLabel(timestamp)
        time_label.setStyleSheet("font-size: 9px; font-family: 'Segoe UI', sans-serif; background: transparent; border: none; color: #64748B; margin-top: 1px;")

        bubble_row = QHBoxLayout()

        if is_self:
            container.setStyleSheet("QWidget { background-color: #8B5CF6; border-radius: 4px; }")
            msg_label.setStyleSheet("font-size: 13px; font-family: 'Segoe UI', sans-serif; background: transparent; border: none; color: #FFFFFF;")
            box_layout.addWidget(msg_label)

            bubble_row.addStretch()
            bubble_row.addWidget(container)

            main_layout.addLayout(bubble_row)
            main_layout.addWidget(time_label, alignment=Qt.AlignmentFlag.AlignRight)
        else:
            container.setStyleSheet("QWidget { background-color: #E2E8F0; border-radius: 4px; }")
            msg_label.setStyleSheet("font-size: 13px; font-family: 'Segoe UI', sans-serif; background: transparent; border: none; color: #1E1B4B;")
            box_layout.addWidget(msg_label)

            bubble_row.addWidget(container)
            bubble_row.addStretch()

            main_layout.addLayout(bubble_row)
            main_layout.addWidget(time_label, alignment=Qt.AlignmentFlag.AlignLeft)


class Main_Chatroom(QMainWindow):
    def __init__(self, user_id, username='Guest'):
        super().__init__()
        self.username = username
        self.user_id = user_id
        self.receiver_id = None
        self.user_avatar = ""
        
        user_info = get_user_by_id(self.user_id)
        if user_info:
            self.username = user_info[1]
            self.user_avatar = user_info[2] or ""

        self.title = f"Local Chatroom - Logged in as: {self.username}"
        self.x = 200
        self.y = 200
        self.width = 750
        self.height = 450
        self.initUI()
        self.load_contacts()

    # Purple / Blue / Cyan Theme Color Palette
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #F8FAFC;
                color: #1E1B4B;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel { color: #1E1B4B; }
            QListWidget#contactsWidget {
                background-color: #FFFFFF;
                color: #1E1B4B;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                font-size: 14px;
                padding: 5px;
            }
            QListWidget#contactsWidget::item { border-radius: 6px; margin-bottom: 2px; }
            QListWidget#contactsWidget::item:selected { background-color: #E2E8F0; }
            QListWidget#chatWidget {
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                background-color: #FFFFFF;
            }
            QListWidget#chatWidget::item { border: none; background: transparent; }
            QListWidget#chatWidget::item:selected { background: transparent; }
            QLineEdit {
                background-color: #FFFFFF;
                color: #1E1B4B;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QPushButton#sendBtn {
                background-color: #8B5CF6;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton#sendBtn:hover { background-color: #7C3AED; }
            QPushButton#emojiBtn {
                background-color: #3B82F6;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }
            QPushButton#emojiBtn:hover { background-color: #2563EB; }
            QPushButton#profileBtn {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 16px;
                padding: 4px 10px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton#profileBtn:hover { background-color: #E2E8F0; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)

        # Header Bar
        top_bar = QHBoxLayout()
        app_title = QLabel("Local Chatroom")
        app_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #8B5CF6;")

        self.profile_btn = QPushButton()
        self.profile_btn.setObjectName("profileBtn")
        self.profile_btn.setToolTip("Edit Profile")
        self.profile_btn.clicked.connect(self.open_profile_dialog)
        self.refresh_profile_header()

        top_bar.addWidget(app_title)
        top_bar.addStretch()
        top_bar.addWidget(self.profile_btn)

        main_layout.addLayout(top_bar)

        content_layout = QHBoxLayout()

        # Chats / Users
        self.user_chats = QVBoxLayout()
        self.chats_display = QLabel("Chats")
        self.chats_display.setStyleSheet("font-weight: bold; font-size: 15px;")
        self.user_chats.addWidget(self.chats_display)

        self.contacts = QListWidget()
        self.contacts.setObjectName("contactsWidget")
        self.contacts.itemClicked.connect(self.select_contacts)
        self.user_chats.addWidget(self.contacts)

        contacts_list = QWidget()
        contacts_list.setLayout(self.user_chats)
        contacts_list.setMaximumWidth(200)
        content_layout.addWidget(contacts_list)

        # Main Chat System
        chat_area = QVBoxLayout()

        self.chat_display = QListWidget()
        self.chat_display.setObjectName("chatWidget")
        self.chat_display.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        chat_area.addWidget(self.chat_display)

        send_text = QHBoxLayout()
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type a message (max 300 characters)...")
        self.text_input.setMaxLength(300)
        self.text_input.returnPressed.connect(self.send_message)
        send_text.addWidget(self.text_input)

        self.emojiButton = QPushButton("😊")
        self.emojiButton.setObjectName("emojiBtn")
        self.emojiButton.setFixedWidth(30)
        self.emojiButton.setFixedHeight(30)
        self.emojiButton.clicked.connect(self.open_emoji_picker)
        send_text.addWidget(self.emojiButton)

        self.sendButton = QPushButton("Send")
        self.sendButton.setObjectName("sendBtn")
        self.sendButton.clicked.connect(self.send_message)
        send_text.addWidget(self.sendButton)

        chat_area.addLayout(send_text)

        chat_area_display = QWidget()
        chat_area_display.setLayout(chat_area)
        content_layout.addWidget(chat_area_display)

        main_layout.addLayout(content_layout)
        self.show()

    def refresh_profile_header(self):
        user_info = get_user_by_id(self.user_id)
        if user_info:
            self.username = user_info[1]
            self.user_avatar = user_info[2] or ""

        pix = get_circular_pixmap(self.user_avatar, size=24)
        if pix:
            self.profile_btn.setIcon(QIcon(pix))
            self.profile_btn.setIconSize(QtCore.QSize(24, 24))
            self.profile_btn.setText(f" {self.username}")
        else:
            self.profile_btn.setIcon(QIcon())
            self.profile_btn.setText(f"👤 {self.username}")

        self.setWindowTitle(f"Chatroom - Logged in as: {self.username}")

    def open_profile_dialog(self):
        dialog = ProfileDialog(self.user_id, self.username, self.user_avatar, self)
        if dialog.exec():
            self.refresh_profile_header()
            self.load_contacts()

    def open_emoji_picker(self):
        picker = EmojiPicker(self)
        if picker.exec() and picker.selected_emoji:
            self.text_input.setText(self.text_input.text() + picker.selected_emoji)
            self.text_input.setFocus()

    def load_contacts(self):
        self.contacts.clear()

        for user_data in get_all_users():
            user_id = user_data[0]
            username = user_data[1]
            avatar_path = user_data[2] if len(user_data) > 2 else ""

            if int(user_id) == self.user_id:
                continue

            contact_widget = ContactItemWidget(username, avatar_path)
            item = QListWidgetItem(self.contacts)
            item.setData(Qt.ItemDataRole.UserRole, int(user_id))
            item.setText("")  # Clears underlying default text rendering behind custom widget
            item.setSizeHint(contact_widget.sizeHint())

            self.contacts.addItem(item)
            self.contacts.setItemWidget(item, contact_widget)

    def select_contacts(self, item):
        self.receiver_id = int(item.data(Qt.ItemDataRole.UserRole))
        self.chat_display.clear()

        for msg in get_messages(self.user_id, self.receiver_id):
            message_id, sender_id, receiver_id, message, timestamp = msg
            is_self = (int(sender_id) == self.user_id)

            bubble_widget = MessageBubble(message, timestamp, is_self)
            list_item = QListWidgetItem(self.chat_display)
            list_item.setSizeHint(bubble_widget.sizeHint())

            self.chat_display.addItem(list_item)
            self.chat_display.setItemWidget(list_item, bubble_widget)

        self.chat_display.scrollToBottom()

    def send_message(self):
        message = self.text_input.text().strip()

        if not message:
            return
        
        if self.receiver_id is None:
            QMessageBox.warning(self, "No Recipient", "Please Select a contact first.")
            return

        save_message(self.user_id, self.receiver_id, message)
        self.text_input.clear()
        
        if self.contacts.currentItem():
            self.select_contacts(self.contacts.currentItem())

    def logout(self):
        self.menu = App()
        self.menu.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_Chatroom(user_id=1, username='TestUser')
    sys.exit(app.exec())

import sys
import os 
import csv
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidget, QListWidgetItem)

from AccountRegistration import RegistrationApp
from database import save_message, get_all_users, get_messages

CSV_file = "accounts.csv"

class Main_Chatroom(QMainWindow):
    def __init__(self, user_id, username = 'Guest'):
        super().__init__()
        self.username = username
        self.user_id = user_id 
        self.receiver_id = None
        self.title = f"Chatroom - Logged in as: {self.username}"
        self.x = 200
        self.y = 200
        self.width = 750
        self.height = 450
        self.initUI()
        self.load_contacts()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_systems = QHBoxLayout(central_widget)

        # Chats / Users
        self.user_chats = QVBoxLayout()
        self.chats_display = QLabel("Chats")
        self.chats_display.setStyleSheet("font-weight: bold; font-size: 15px;")
        self.user_chats.addWidget(self.chats_display)

        self.contacts = QListWidget()
        self.contacts.itemClicked.connect(self.select_contacts)
        self.user_chats.addWidget(self.contacts)

        contacts_list = QWidget()
        contacts_list.setLayout(self.user_chats)
        contacts_list.setMaximumWidth(200)
        main_systems.addWidget(contacts_list)

        # Main Chat System
        chat_area = QVBoxLayout()

        self.chat_display = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("Chat History will appear here...")
        chat_area.addWidget(self.chat_display)

        send_text = QHBoxLayout()
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type a message (max 300 characters)...")
        self.text_input.setMaxLength(300)

        self.text_input.returnPressed.connect(self.send_message)
        send_text.addWidget(self.text_input)

        self.sendButton = QPushButton("Send (>)")
        self.sendButton.clicked.connect(self.send_message)
        send_text.addWidget(self.sendButton)

        chat_area.addLayout(send_text)

        chat_area_display = QWidget()
        chat_area_display.setLayout(chat_area)
        main_systems.addWidget(chat_area_display)

        self.show()

    def load_contacts(self):
        self.contacts.clear()

        for user_id, username in get_all_users():
            if user_id == self.user_id:
                continue
            item = QListWidgetItem(username)
            item.setData(Qt.ItemDataRole.UserRole,user_id)
            self.contacts.addItem(item)

    def select_contacts(self,item):
        self.receiver_id = item.data(Qt.ItemDataRole.UserRole)

        self.chat_display.clear()

        for msg in get_messages(self.user_id, self.receiver_id):
            message_id, sender_id, receiver_id, message, timestamp = msg

            sender=(
                self.username
                if sender_id == self.user_id
                else item.text()
            )

            self.chat_display.append(
                f"<b>{sender}:</b> {message} <small>{timestamp}</small>"
            )

    def send_message(self):
        message = self.text_input.text().strip()

        if not message:
            return
        
        if self.receiver_id is None:
            QMessageBox.warning(self,"No Recipient","Please Select a contact first.")
            return

        
        save_message(self.user_id,self.receiver_id,message)
        self.text_input.clear()
        self.select_contacts(self.contacts.currentItem())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_Chatroom()
    sys.exit(app.exec())

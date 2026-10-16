import sqlite3

def create_tables():
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()

def create_user(username, password):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (?, ?)
    """, (username, password))

    connection.commit()
    connection.close()
    return True

def get_user(username):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username, password
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    connection.close()

    return user

def get_all_users():
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username
        FROM users
        ORDER BY username ASC
    """)
    users = cursor.fetchall()
    connection.close()

    return users

def save_message(sender_id, receiver_id, message):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages (sender_id, receiver_id, message)
        VALUES (?, ?, ?)
    """, (sender_id, receiver_id, message))

    connection.commit()
    connection.close()

def get_messages(id1,id2):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, sender_id, receiver_id, message, timestamp
        FROM messages
        WHERE
            (sender_id = ? AND receiver_id = ?)
            OR
            (sender_id = ? AND receiver_id = ?)
        ORDER BY timestamp ASC
    """,(id1,id2,id2,id1))

    messages = cursor.fetchall()

    connection.close()
    return messages 

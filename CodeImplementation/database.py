import sqlite3

# Initialize database tables for users and messages, including avatar support
def create_tables():
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            avatar TEXT DEFAULT ''
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

# Save a newly registered user account to the database
def create_user(username, password):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, password))
        connection.commit()
        connection.close()
        return True, "Account registered successfully!"
    except sqlite3.IntegrityError:
        connection.close()
        return False, "Username already exists. Please choose another."

# Retrieve a single user record by username
def get_user(username, password=None):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    if password is not None:
        cursor.execute("""
            SELECT id, username, password 
            FROM users
            WHERE username = ? AND password = ?
        """, (username, password))
    else:
        cursor.execute("""
            SELECT id, username, password
            FROM users
            WHERE username = ?
        """, (username,))

    user = cursor.fetchone()
    connection.close()
    return user

# Retrieve user details including avatar path by user ID
def get_user_by_id(user_id):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, username, avatar FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    connection.close()
    return user

# Update a user's username
def update_username(user_id, new_username):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
        connection.commit()
        connection.close()
        return True, "Username updated successfully!"
    except sqlite3.IntegrityError:
        connection.close()
        return False, "Username already taken. Choose another."

# Update a user's avatar file path
def update_user_avatar(user_id, avatar_path):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET avatar = ? WHERE id = ?", (avatar_path, user_id))
    connection.commit()
    connection.close()

# Retrieve all registered users sorted alphabetically
def get_all_users():
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username, avatar
        FROM users
        ORDER BY username ASC
    """)
    users = cursor.fetchall()
    connection.close()

    return users

# Save chat message to database
def save_message(sender_id, receiver_id, message):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages (sender_id, receiver_id, message)
        VALUES (?, ?, ?)
    """, (sender_id, receiver_id, message))

    connection.commit()
    connection.close()

# Retrieve message history between two users
def get_messages(id1, id2):
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
    """, (id1, id2, id2, id1))

    messages = cursor.fetchall()
    connection.close()
    return messages
import sqlite3

connection = sqlite3.connect("userdb.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    chatid TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    apppass TEXT
)
''')

def save_chat_id(chat_id):
    cursor.execute(f"INSERT INTO users (chatid, email, apppass) VALUES (?, ?, ?)", (f"{chat_id}", None, None))
    connection.commit()
    
def delete_user_email(email):
    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    connection.commit()
    
def show_all_users():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return rows
    
def update_user(chat_id, email, apppass):
    cursor.execute("UPDATE users SET email = ?, apppass = ? WHERE chatid = ?", (email, apppass, chat_id))
    connection.commit()
    
def delete_user_chatid(chat_id):
    cursor.execute("DELETE FROM users WHERE chatid = ?", (chat_id,))
    connection.commit()

def check_user_exists(chat_id):
    cursor.execute("SELECT 1 FROM users WHERE chatid = ?", (chat_id,))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False

def return_email_and_pass(chat_id):
    cursor.execute("SELECT id, chatid, email, apppass FROM users WHERE chatid = ?", (chat_id,))
    result = cursor.fetchone()
    if len(result) == 1:
        print("No Email Pass")
        return None, None
    else:
        return result[2], result[3]
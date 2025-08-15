import sqlite3

DB_PATH = 'messages.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, content TEXT)''')
    conn.commit()
    conn.close()

def add_message(content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO messages (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, content FROM messages ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

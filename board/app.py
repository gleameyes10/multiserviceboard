from flask import Flask, request, render_template, redirect
import sqlite3
import os
import logging

app = Flask(__name__)

# Detect if running inside Docker (simple heuristic)
IN_DOCKER = os.path.exists("/.dockerenv")

# Logging setup
try:
    log_dir = "/var/log/app" if IN_DOCKER else os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
except PermissionError:
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "board.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# DB path
DB_PATH = "/app/data/messages.db" if IN_DOCKER else os.path.join(os.path.dirname(__file__), "data", "messages.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    """Create the messages table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  content TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Ensure DB exists
init_db()

@app.before_request
def log_request_info():
    logging.info(f"{request.method} {request.path} from {request.remote_addr}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        if content.strip():
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO messages (content) VALUES (?)", (content,))
            conn.commit()
            conn.close()
            logging.info(f"Message added: {content}")
        return redirect('/')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, content FROM messages ORDER BY id DESC")
    messages = c.fetchall()
    conn.close()
    
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


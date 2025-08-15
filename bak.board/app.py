from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import logging
from models import init_db, add_message, get_messages

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DB
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            add_message(content)
            logger.info("Added message: %s", content)
        else:
            logger.warning("Empty message submission ignored")
        return redirect(url_for("index"))
    messages = get_messages()
    return render_template("index.html", messages=messages)

@app.route("/healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

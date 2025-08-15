import os
import sqlite3
import pytest
from board.app import app, DB_PATH

@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_post_message(test_client):
    # Allow custom test message via environment variable
    custom_message = os.environ.get("TEST_MESSAGE", "Hello Test")

    response = test_client.post("/", data={"content": custom_message})
    assert response.status_code == 302  # Redirect after posting

    # Verify the message is stored in the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT content FROM messages ORDER BY id DESC LIMIT 1")
    last_message = c.fetchone()[0]
    conn.close()

    assert last_message == custom_message

def test_retrieve_message_from_db(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data  # crude check that page rendered


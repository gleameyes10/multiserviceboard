import pytest
from monitor.app import app
import sqlite3
import os

@pytest.fixture
def test_client():
    with app.test_client() as client:
        yield client

def test_metrics_endpoint(test_client):
    """Test that /metrics returns JSON with CPU, MEM, DISK keys."""
    response = test_client.get("/metrics")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "cpu_percent" in data
    assert "mem_percent" in data
    assert "disk_percent" in data

def test_healthz_endpoint(test_client):
    """Test that /healthz returns JSON with status 'ok'."""
    response = test_client.get("/healthz")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"status": "ok"}

def test_production_db_has_messages():
    """
    Check that the production DB has at least one message.
    This only works if the data/messages.db file is mounted from the live container.
    """
    db_path = os.path.join("data", "messages.db")
    assert os.path.exists(db_path), "DB file not found"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM messages")
    count = cursor.fetchone()[0]
    conn.close()
    assert count > 0, "Production DB has no messages"


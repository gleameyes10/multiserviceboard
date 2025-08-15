from flask import Flask, jsonify, request
import psutil
import os
import logging

app = Flask(__name__)

# Logging setup — default to ./logs if LOG_DIR not set
LOG_DIR = os.environ.get("LOG_DIR", "./logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "monitor.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@app.before_request
def log_request_info():
    logging.info(f"{request.method} {request.path} from {request.remote_addr}")

@app.route("/")
def index():
    logging.info("Monitor root page accessed")

    # Get metrics
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # Get health
    health_status = "ok"

    return f"""
    <html>
    <head><title>Monitor Service</title></head>
    <body>
        <h1>Monitor Service</h1>
        <h2>System Metrics</h2>
        <ul>
            <li>CPU Usage: {cpu}%</li>
            <li>Memory Usage: {mem}%</li>
            <li>Disk Usage: {disk}%</li>
        </ul>
        <h2>Health Check</h2>
        <p>Status: {health_status}</p>
    </body>
    </html>
    """

@app.route("/metrics")
def metrics():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    logging.info(f"Metrics requested: CPU={cpu}%, MEM={mem}%, DISK={disk}%")

    return jsonify(
        cpu_percent=cpu,
        mem_percent=mem,
        disk_percent=disk,
        cpu=cpu,
        memory=mem,
        disk=disk
    )

@app.route("/healthz")
def healthz():
    logging.info("Health check requested")
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)


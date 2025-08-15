# Multi-Service Text Board Platform

## Services
- **board**: Simple Flask-based text board with SQLite persistence.
- **monitor**: Reports CPU, memory, disk usage using psutil.
- **nginx**: Reverse proxy.

## Usage
```bash
docker compose up --build
```
Visit:
- http://localhost/ -> Text Board
- http://localhost/monitor/metrics -> Metrics JSON
```

### Notes
- `pid: "host"` in monitor allows host-level metrics. Remove if not needed.
- Messages are stored in SQLite DB inside board container volume.

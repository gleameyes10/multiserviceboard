- **Text Board** — simple web app to post and view messages (persistent storage)
- **Monitoring Service** — shows CPU, memory, and disk usage of the host

---

## Requirements

- Docker  
- Docker Compose  
- Git  

---

### Install Docker & Docker Compose

james@james:~/multi-service-text-board-full$ docker --version
Docker version 27.3.1, build ce12230
james@james:~/multi-service-text-board-full$ docker compose version
Docker Compose version v2.3.3



## How to Run

1. **Clone this repository**
   ```bash
   git clone https://github.com/gleameyes10/multiserviceboard.git
   cd multiserviceboard
   ```

2. **Build and start all services**
   ```bash
   docker compose up --build
   ```
   > If your system uses the old `docker-compose` command:
   ```bash
   docker-compose up --build
   ```

3. **Access the applications**
   - **Text Board:** [http://localhost:50080/](http://localhost:50080/)  
   - **Monitoring Dashboard:** [http://localhost:50080/monitor/](http://localhost:50080/monitor/)  

---

## Services

| Service           | Description                               | Internal Port | Public Path via Nginx |
|-------------------|-------------------------------------------|---------------|-----------------------|
| board             | Python Flask app to post/view messages    | 5000          | `/`                   |
| monitor           | Python Flask app to show system metrics   | 5001          | `/monitor/`           |
| nginx             | Reverse proxy routing board & monitor     | 80            | mapped to host:50080  |

---

## Running Tests

james@james:~/multi-service-text-board-full$ TEST_MESSAGE="This is my test message" PYTHONPATH=. pytest -v
===================================================================== test session starts ======================================================================
platform linux -- Python 3.8.10, pytest-8.3.5, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/james/multi-service-text-board-full
collected 5 items                                                                                                                                              

tests/test_board.py::test_post_message PASSED                                                                                                            [ 20%]
tests/test_board.py::test_retrieve_message_from_db PASSED                                                                                                [ 40%]
tests/test_monitor.py::test_metrics_endpoint PASSED                                                                                                      [ 60%]
tests/test_monitor.py::test_healthz_endpoint PASSED                                                                                                      [ 80%]
tests/test_monitor.py::test_production_db_has_messages PASSED                                                                                            [100%]

====================================================================== 5 passed in 0.64s =======================================================================


## DB is stored inside docker container
james@james:~/multi-service-text-board-full$ docker cp board:/app/data/messages.db ./messages.db
Successfully copied 13.8kB to /home/james/multi-service-text-board-full/messages.db
james@james:~/multi-service-text-board-full$ sqlite3 messages.db
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
sqlite> SELECT * FROM messages;
1|Hi
2|Good Day


---

## Versions Used in Development

| Tool / Library  | Version |
|-----------------|---------|
| Docker          | *(check via `docker --version`)* |
| Docker Compose  | *(check via `docker compose version`)* |
| Python          | *(check via `python3 --version`)* |
| Gunicorn        | *(inside `board` container)* |
| Flask           | *(inside both containers)* |
| psutil          | *(inside `monitor` container)* |

---

##Stop, Start, Restart Dockers
james@james:~/multi-service-text-board-full$ docker start monitor nginx board
james@james:~/multi-service-text-board-full$ docker stop monitor nginx board
vjames@james:~/multi-service-text-board-full$ docker restart monitor nginx board


## Notes

- Messages are stored in a SQLite database mounted to a Docker volume, so they persist between container restarts. docker compose down -v will erase the entire volume including the messages so one must not use the -v option.
- Python apps run in **production mode** using Gunicorn (not debug mode).
- Reverse proxy is handled by **Nginx**, routing `/` to the board and `/monitor/` to the monitor.
- Logs and health checks are implemented.

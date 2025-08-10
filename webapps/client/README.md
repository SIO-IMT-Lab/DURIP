# Client Web Application

Client-facing FastAPI service for viewing and modifying sensor schedules. The
implementation reuses shared logic and assets located in the sibling
`webapps/shared` directory.

## Project Layout

```text
client/
├── __init__.py
├── main.py   # FastAPI application entry point
└── README.md
```

## Running the Web Application

Install dependencies and start the server using `uvicorn` with the module path:

```bash
pip install fastapi uvicorn python-crontab
uvicorn webapps.client.main:app --reload
```

Then browse to <http://localhost:8000> to access the interface.

Assets, helper scripts and the `ScheduleManager` implementation live under
`webapps/shared` and are automatically referenced by the application.


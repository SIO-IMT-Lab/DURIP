# Admin Web Application

Administrative counterpart to the client web interface. It exposes the same
features but protects all routes with HTTP Basic authentication.

## Project Layout

```text
admin/
├── __init__.py
├── main.py   # FastAPI app with Basic auth
└── README.md
```

## Running the Web Application

Create a `.env` file with credentials and launch using `uvicorn`:

```bash
pip install fastapi uvicorn python-crontab python-dotenv
echo -e "USERNAME=admin\nPASSWORD=secret" > .env
uvicorn webapps.admin.main:app --reload
```

Navigate to <http://localhost:8000> and provide the configured username and
password when prompted.

The application relies on shared assets and scheduling logic found in
`webapps/shared`.


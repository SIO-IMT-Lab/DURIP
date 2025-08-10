"""Admin-facing FastAPI application with HTTP Basic authentication."""

from pathlib import Path
import os
import shutil

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from ..shared.services.schedule_manager import ScheduleManager

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shared"

app = FastAPI()
app.mount("/static", StaticFiles(directory=SHARED_DIR / "static"), name="static")
security = HTTPBasic()
manager = ScheduleManager()


class CommandRequest(BaseModel):
    command: str
    args: list[str] = []


def authenticate(credentials: HTTPBasicCredentials = Depends(security)) -> HTTPBasicCredentials:
    correct_username = credentials.username == USERNAME
    correct_password = credentials.password == PASSWORD
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials


@app.get("/", response_class=HTMLResponse)
async def read_root(credentials: HTTPBasicCredentials = Depends(authenticate)) -> HTMLResponse:
    with open(SHARED_DIR / "static" / "index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/execute")
async def execute_command(
    request: CommandRequest, credentials: HTTPBasicCredentials = Depends(authenticate)
) -> HTMLResponse:
    result = manager.execute(request.command, request.args)
    return HTMLResponse(content=result)


@app.get("/view_schedules")
async def view_schedules(credentials: HTTPBasicCredentials = Depends(authenticate)) -> HTMLResponse:
    return HTMLResponse(content=manager.view_schedules())


@app.get("/view_states")
async def view_states(credentials: HTTPBasicCredentials = Depends(authenticate)) -> HTMLResponse:
    return HTMLResponse(content=manager.view_states())


@app.post("/upload_schedule")
async def upload_schedule(
    file: UploadFile = File(...),
    credentials: HTTPBasicCredentials = Depends(authenticate),
) -> HTMLResponse:
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="File must be a JSON file")
    schedule_dir = SHARED_DIR / "schedule_files"
    temp_path = schedule_dir / file.filename
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    existing = schedule_dir / "sensor_schedule.json"
    backup_dir = schedule_dir / "on_hold"
    backup_dir.mkdir(exist_ok=True)
    if existing.exists():
        existing.rename(backup_dir / "sensor_schedule.json")
    temp_path.rename(existing)
    return HTMLResponse(content=manager.view_schedules())


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil

from services.schedule_manager import ScheduleManager

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
manager = ScheduleManager()


class CommandRequest(BaseModel):
    command: str
    args: list[str] = []


@app.get("/", response_class=HTMLResponse)
async def read_root() -> HTMLResponse:
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/execute")
async def execute_command(request: CommandRequest) -> HTMLResponse:
    try:
        result = manager.execute(request.command, request.args)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return HTMLResponse(content=result)


@app.get("/view_schedules")
async def view_schedules() -> HTMLResponse:
    return HTMLResponse(content=manager.view_schedules())


@app.get("/view_states")
async def view_states() -> HTMLResponse:
    return HTMLResponse(content=manager.view_states())


@app.post("/upload_schedule")
async def upload_schedule(file: UploadFile = File(...)) -> dict:
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="File must be a JSON file")
    with open(f"schedule_files/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

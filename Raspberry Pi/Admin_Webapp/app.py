from fastapi import FastAPI, Form, HTTPException, File, UploadFile, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import subprocess
import uvicorn
import shutil
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

app = FastAPI()
security = HTTPBasic()

app.mount("/static", StaticFiles(directory="static"), name="static")

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = credentials.username == USERNAME
    correct_password = credentials.password == PASSWORD

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

def run_sensor_schedule_command(command):
    """Run sensor_schedule.py with the specified command."""
    result = subprocess.run(['python', 'sensor_schedule.py'] + command, capture_output=True, text=True)
    return result.stdout

@app.get("/", response_class=HTMLResponse)
async def read_root(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return HTMLResponse(content=open("static/index.html", "r").read(), status_code=200)

@app.post("/execute")
async def execute_command(input_value: dict, credentials: HTTPBasicCredentials = Depends(authenticate)):
    command = input_value["command"]
    args = input_value["args"]
    args_list = args.split(',') if args else []
    print(f"Command: {command}, Args: {args_list}")
    result = run_sensor_schedule_command([command] + args_list)
    return result

@app.get("/view_schedules")
async def view_schedules(credentials: HTTPBasicCredentials = Depends(authenticate)):
    result = run_sensor_schedule_command(['view'])
    return HTMLResponse(content=result, status_code=200)

@app.get("/view_states")
async def view_states(credentials: HTTPBasicCredentials = Depends(authenticate)):
    result = run_sensor_schedule_command(['view_states'])
    return HTMLResponse(content=result, status_code=200)

@app.post("/upload_schedule")
async def create_upload_file(file: UploadFile = File(...), credentials: HTTPBasicCredentials = Depends(authenticate)):
    if file.filename.split('.')[-1] != "json":
        raise HTTPException(status_code=400, detail="File must be a JSON file")
    
    with open(f"schedule_files/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        if os.path.exists("schedule_files/sensor_schedule.json"):
            os.rename("schedule_files/sensor_schedule.json", "schedule_files/on_hold/sensor_schedule.json")

        os.rename(f"schedule_files/{file.filename}", "schedule_files/sensor_schedule.json")

    result = run_sensor_schedule_command(['view'])
    return HTMLResponse(content=result, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
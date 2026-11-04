"""Local demonstration API. No authentication or real model is configured."""
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from app.service import WorkflowService

BASE = Path(__file__).resolve().parent


class NewTask(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=3000)

    @field_validator("title", "description")
    @classmethod
    def nonblank(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Este campo es obligatorio")
        return value


class Review(BaseModel):
    decision: Literal["approve", "reject"]
    note: str = Field(default="", max_length=2000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.service = WorkflowService(Path(os.environ.get("APF_DATA_DIR", "data")))
    yield
    app.state.service.close()


app = FastAPI(title="APF · prototipo local", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/")
def home():
    return FileResponse(BASE / "static" / "index.html")


@app.get("/api/tasks")
def tasks(request: Request):
    return request.app.state.service.list()


@app.post("/api/tasks", status_code=201)
def create_task(payload: NewTask, request: Request):
    return request.app.state.service.create(payload.title, payload.description)


@app.get("/api/tasks/{task_id}")
def get_task(task_id: str, request: Request):
    try:
        return request.app.state.service.get(task_id)
    except KeyError:
        raise HTTPException(404, "Tarea no encontrada")


@app.post("/api/tasks/{task_id}/review")
def review(task_id: str, payload: Review, request: Request):
    try:
        return request.app.state.service.decide(task_id, payload.decision, payload.note.strip())
    except KeyError:
        raise HTTPException(404, "Tarea no encontrada")
    except ValueError as exc:
        raise HTTPException(409, str(exc))

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
    instance: str = Field(default="readiness-test", max_length=41)
    series: str | None = Field(default=None, max_length=41)
    criteria: list[str] | None = Field(default=None, max_length=20)
    invariants: list[str] = Field(default_factory=list, max_length=20)
    scope: list[str] | None = Field(default=None, max_length=20)
    next_item: str = Field(default="END", max_length=32)
    auto_arm: bool = True

    @field_validator("title", "description")
    @classmethod
    def nonblank(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Este campo es obligatorio")
        return value


class Review(BaseModel):
    decision: Literal["approve", "reject", "amend"]
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
    try:
        return request.app.state.service.create(payload.title, payload.description, instance=payload.instance,
            series=payload.series, criteria=payload.criteria, invariants=payload.invariants, scope=payload.scope,
            next_item=payload.next_item, auto_arm=payload.auto_arm)
    except ValueError as exc:
        raise HTTPException(422, str(exc))


@app.get("/api/tasks/{task_id}")
def get_task(task_id: str, request: Request):
    try:
        return request.app.state.service.get(task_id)
    except KeyError:
        raise HTTPException(404, "Tarea no encontrada")


@app.post("/api/tasks/{task_id}/arm")
def arm(task_id: str, request: Request):
    try:
        return request.app.state.service.arm(task_id)
    except KeyError:
        raise HTTPException(404, "Tarea no encontrada")
    except ValueError as exc:
        raise HTTPException(409, str(exc))


@app.post("/api/tasks/{task_id}/review")
def review(task_id: str, payload: Review, request: Request):
    try:
        return request.app.state.service.decide(task_id, payload.decision, payload.note.strip())
    except KeyError:
        raise HTTPException(404, "Tarea no encontrada")
    except ValueError as exc:
        raise HTTPException(409, str(exc))


@app.get("/api/control")
def control(request: Request):
    return {"paused": request.app.state.service.is_paused(), "executor": os.environ.get("APF_EXECUTOR", "simulated")}


@app.post("/api/control/{action}")
def set_control(action: Literal["pause", "resume"], request: Request):
    return request.app.state.service.set_paused(action == "pause")


@app.get("/api/artifacts")
def artifacts(request: Request):
    return request.app.state.service.artifacts()

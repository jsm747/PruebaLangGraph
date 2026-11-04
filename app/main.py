"""APF proof-of-concept API: guided Builder and optional configured models."""
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from app.service import WorkflowService
from app.builder import BuilderService
from app.executor import ExecutionError

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
    app.state.builder = BuilderService(app.state.service)
    yield
    app.state.service.close()


app = FastAPI(title="APF · prototipo local", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/")
def home():
    return FileResponse(BASE / "static" / "builder.html")


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


@app.get("/tasks")
def task_workspace():
    return FileResponse(BASE / "static" / "index.html")


class BuilderStart(BaseModel):
    name: str = Field(min_length=1,max_length=120)


class BuilderAnswer(BaseModel):
    revision: int = Field(ge=0)
    answers: dict[str,str] = Field(default_factory=dict)
    text: str = Field(default="",max_length=12000)


class BuilderConfirm(BaseModel):
    revision: int = Field(ge=0)


class CaseInput(BaseModel):
    title: str = Field(min_length=1,max_length=120)
    data: str = Field(min_length=1,max_length=3000)


class ImprovementInput(BaseModel):
    observation: str = Field(min_length=1,max_length=4000)
    change: str = Field(min_length=1,max_length=4000)
    metric: str = Field(min_length=1,max_length=4000)
    target: str = Field(min_length=1,max_length=4000)
    due: str


class ImprovementRuling(BaseModel):
    decision: Literal['approved','closed']
    reason: str = Field(min_length=1,max_length=2000)


def builder_call(fn,*args):
    try:
        return fn(*args)
    except KeyError:
        raise HTTPException(404,'Sesión, instancia o caso no encontrado.')
    except (ValueError, ExecutionError) as exc:
        raise HTTPException(409,str(exc))


@app.get('/api/builder')
def builder_list(request:Request):
    return request.app.state.builder.list()


@app.post('/api/builder',status_code=201)
def builder_start(payload:BuilderStart,request:Request):
    if not payload.name.strip(): raise HTTPException(422,'Indica un nombre.')
    return request.app.state.builder.create(payload.name.strip())


@app.get('/api/builder/{sid}')
def builder_get(sid:str,request:Request):
    return builder_call(request.app.state.builder.get,sid)


@app.post('/api/builder/{sid}/answer')
def builder_answer(sid:str,payload:BuilderAnswer,request:Request):
    return builder_call(request.app.state.builder.answer,sid,payload.revision,payload.answers,payload.text)


@app.post('/api/builder/{sid}/confirm')
def builder_confirm(sid:str,payload:BuilderConfirm,request:Request):
    return builder_call(request.app.state.builder.confirm,sid,payload.revision)


@app.post('/api/builder/{sid}/first-run')
def builder_first_run(sid:str,request:Request):
    return builder_call(request.app.state.builder.first_run,sid)


@app.get('/api/builder/{sid}/export')
def builder_export(sid:str,request:Request):
    import io,json,zipfile
    from fastapi.responses import StreamingResponse
    state=builder_call(request.app.state.builder.get,sid)
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as archive:
        for path,content in state['artifacts'].items(): archive.writestr(path,content)
        archive.writestr('builder-session.json',json.dumps(state,ensure_ascii=False,indent=2))
    buffer.seek(0)
    return StreamingResponse(buffer,media_type='application/zip',headers={'Content-Disposition':f'attachment; filename="{sid}.zip"'})


@app.post('/api/instances/{sid}/cases',status_code=201)
def instance_case(sid:str,payload:CaseInput,request:Request):
    return builder_call(request.app.state.builder.create_case,sid,payload.title,payload.data)


@app.get('/api/instances/{sid}/audit')
def instance_audit(sid:str,request:Request):
    return builder_call(request.app.state.builder.audit,sid)


@app.get('/api/instances/{sid}/improvements')
def improvement_list(sid:str,request:Request):
    return builder_call(request.app.state.builder.proposals,sid)


@app.post('/api/instances/{sid}/improvements',status_code=201)
def improvement_create(sid:str,payload:ImprovementInput,request:Request):
    return builder_call(request.app.state.builder.propose,sid,payload.model_dump())


@app.post('/api/instances/{sid}/improvements/{pid}/ruling')
def improvement_ruling(sid:str,pid:str,payload:ImprovementRuling,request:Request):
    return builder_call(request.app.state.builder.rule,sid,pid,payload.decision,payload.reason)

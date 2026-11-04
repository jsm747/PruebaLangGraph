"""A LangGraph workflow adapted from the APF pilot; execution is simulated."""
from typing import Annotated, Literal, TypedDict
import operator
import os
import uuid
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt
from app.checks import check_proposal
from app.ingest import ingest
from app.executor import ExecutionError, execute


class TaskState(TypedDict, total=False):
    task_id: str
    title: str
    description: str
    contract: dict
    status: str
    sanitized: dict
    ingestion: dict
    base_files: dict
    files: dict
    proposal: str
    checks: dict
    delivery_scope: list[str]
    execution: dict
    session_id: str
    session_backend: str
    blocked_reason: str
    polarity: str
    derived: list
    decision: str
    review_note: str
    feedback: str
    events: Annotated[list[str], operator.add]


def prepare(state: TaskState) -> dict:
    return {"status": "executing", "decision": "", "review_note": "", "blocked_reason": "",
            "checks": {}, "files": {}, "execution": {}, "delivery_scope": [],
            "session_id": uuid.uuid4().hex, "session_backend": os.environ.get("APF_EXECUTOR", "simulated"),
            "events": ["Ejecutando: contrato admitido; comienza la sesión del ejecutor."]}


def screen(state: TaskState) -> dict:
    contract = state["contract"]
    clean = {}
    reports = {}
    for key, raw in {"title": state["title"], "description": state["description"],
                     "criteria": "\n".join(contract["criteria"]),
                     "invariants": "\n".join(contract["invariants"]),
                     "feedback": state.get("feedback", "")}.items():
        clean[key], reports[key] = ingest(raw)
    flagged = sum(len(report["flagged_lines"]) for report in reports.values())
    masked = sum(sum(report["masked"].values()) for report in reports.values())
    return {"sanitized": clean, "ingestion": reports,
            "events": [f"Pasarela de entrada: {masked} coincidencias enmascaradas, {flagged} líneas señaladas."]}


def generate(state: TaskState) -> dict:
    try:
        result = execute(state["sanitized"], state["contract"], state.get("base_files", {}))
    except ExecutionError as exc:
        return {"status": "blocked", "blocked_reason": str(exc),
                "execution": {"backend": "execution-error", "cost_usd": 0.0, "cost_known": exc.cost_known},
                "events": [f"Ejecutor bloqueado: {exc}"]}
    if result["blocked"]:
        return {"status": "blocked", "blocked_reason": result["blocked"], "execution": result["execution"],
                "events": ["El ejecutor se bloqueó ante una decisión que no pudo derivar."]}
    files = result["files"]
    proposal = "\n\n".join(content for content in files.values())
    return {"proposal": proposal, "files": files, "delivery_scope": result["scope"],
            "execution": result["execution"], "polarity": result["polarity"], "derived": result["derived"],
            "events": ["El ejecutor preparó una propuesta y declaró su alcance."]}


def after_generate(state: TaskState) -> Literal["check", "end"]:
    return "end" if state["status"] == "blocked" else "check"


def check(state: TaskState) -> dict:
    try:
        results = check_proposal(state.get("base_files", {}), state["files"], state["delivery_scope"])
    except Exception as exc:
        return {"status": "blocked", "checks": {},
                "events": [f"Bloqueada: no se pudieron ejecutar los controles ({type(exc).__name__})."]}
    green = all(c["passed"] for c in results.values())
    return {"status": "proposed", "checks": results,
            "events": ["Controles deterministas: " + ("todos verdes." if green else "hay controles en rojo; no se permite aprobar.")]}


def review(state: TaskState) -> dict:
    decision = interrupt({"message": "Revisa la propuesta y sus controles.", "proposal": state["proposal"],
                          "checks": state["checks"]})
    action, note = decision["decision"], decision.get("note", "")
    if action == "amend":
        return {"status": "amendment-pending", "feedback": note,
                "events": ["Se solicitó una modificación; la integración queda bloqueada."]}
    if action == "reject":
        return {"decision": action, "review_note": note, "status": "queued",
                "events": ["Propuesta rechazada: la tarea vuelve a la cola para una nueva ejecución."]}
    return {"decision": action, "review_note": note, "status": "integrated",
            "events": ["Propuesta aprobada en el entorno local de prueba."]}


def acknowledge(state: TaskState) -> dict:
    return {"events": ["El ejecutor acusa recibo de la modificación y vuelve a preparar la propuesta."]}


def after_checks(state: TaskState) -> Literal["review", "end"]:
    return "review" if state["status"] == "proposed" else "end"


def after_review(state: TaskState) -> Literal["amend", "end"]:
    return "amend" if state["status"] == "amendment-pending" else "end"


def build_graph(checkpointer):
    graph = StateGraph(TaskState)
    for name, fn in (("prepare", prepare), ("screen", screen), ("generate", generate),
                     ("check", check), ("review", review), ("acknowledge", acknowledge)):
        graph.add_node(name, fn)
    graph.add_edge(START, "prepare")
    graph.add_edge("prepare", "screen")
    graph.add_edge("screen", "generate")
    graph.add_conditional_edges("generate", after_generate, {"check": "check", "end": END})
    graph.add_conditional_edges("check", after_checks, {"review": "review", "end": END})
    graph.add_conditional_edges("review", after_review, {"amend": "acknowledge", "end": END})
    graph.add_edge("acknowledge", "prepare")
    return graph.compile(checkpointer=checkpointer)

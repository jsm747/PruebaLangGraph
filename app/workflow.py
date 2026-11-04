"""A single local review workflow with durable LangGraph checkpoints."""
from typing import Annotated, Literal, TypedDict
import operator
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt


class TaskState(TypedDict, total=False):
    title: str
    description: str
    status: str
    proposal: str
    decision: str
    review_note: str
    events: Annotated[list[str], operator.add]


def prepare(state: TaskState) -> dict:
    return {"status": "executing", "events": ["Tarea validada y enviada al ejecutor simulado."]}


def generate(state: TaskState) -> dict:
    # The adapter is deliberately deterministic; it makes no external model call.
    proposal = (f"Propuesta de trabajo: {state['title']}\n\n"
                f"Objetivo: {state['description']}\n\n"
                "1. Revisar el contexto y definir los criterios de aceptación.\n"
                "2. Preparar un borrador con datos sintéticos.\n"
                "3. Presentarlo a una persona para su revisión.")
    return {"proposal": proposal, "events": ["El ejecutor simulado preparó la propuesta."]}


def check(state: TaskState) -> dict:
    if not state.get("proposal", "").strip():
        return {"status": "blocked", "events": ["La propuesta está vacía."]}
    return {"status": "proposed", "events": ["Comprobación básica superada; pendiente de revisión humana."]}


def review(state: TaskState) -> dict:
    result = interrupt({"message": "Revisa la propuesta y decide si la apruebas.", "proposal": state["proposal"]})
    decision = result["decision"]
    return {"decision": decision, "review_note": result.get("note", ""),
            "status": "integrated" if decision == "approve" else "rejected",
            "events": ["Propuesta aprobada por el usuario de prueba." if decision == "approve" else "Propuesta rechazada por el usuario de prueba."]}


def after_check(state: TaskState) -> Literal["review", "end"]:
    return "review" if state["status"] == "proposed" else "end"


def build_graph(checkpointer):
    builder = StateGraph(TaskState)
    builder.add_node("prepare", prepare)
    builder.add_node("generate", generate)
    builder.add_node("check", check)
    builder.add_node("review", review)
    builder.add_edge(START, "prepare")
    builder.add_edge("prepare", "generate")
    builder.add_edge("generate", "check")
    builder.add_conditional_edges("check", after_check, {"review": "review", "end": END})
    builder.add_edge("review", END)
    return builder.compile(checkpointer=checkpointer)

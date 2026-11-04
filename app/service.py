"""Local single-process task index and workflow persistence."""
import sqlite3
import threading
import uuid
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command
from app.workflow import build_graph


class WorkflowService:
    def __init__(self, directory: Path):
        directory.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.conn = sqlite3.connect(str(directory / "prototype.sqlite3"), check_same_thread=False)
        self.conn.execute("CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, title TEXT NOT NULL)")
        self.conn.commit()
        self.graph = build_graph(SqliteSaver(self.conn))

    def close(self):
        self.conn.close()

    @staticmethod
    def config(task_id):
        return {"configurable": {"thread_id": task_id}}

    def get(self, task_id):
        with self.lock:
            row = self.conn.execute("SELECT title FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if row is None:
                raise KeyError(task_id)
            snapshot = self.graph.get_state(self.config(task_id))
            values = dict(snapshot.values)
            return {"id": task_id, "title": row[0], "status": values.get("status", "queued"),
                    "description": values.get("description", ""), "proposal": values.get("proposal", ""),
                    "decision": values.get("decision"), "review_note": values.get("review_note", ""),
                    "events": values.get("events", []), "awaiting_review": bool(snapshot.interrupts)}

    def list(self):
        with self.lock:
            ids = [row[0] for row in self.conn.execute("SELECT id FROM tasks ORDER BY rowid DESC")]
            return [self.get(task_id) for task_id in ids]

    def create(self, title, description):
        with self.lock:
            task_id = uuid.uuid4().hex
            self.conn.execute("INSERT INTO tasks VALUES (?, ?)", (task_id, title))
            self.conn.commit()
            self.graph.invoke({"title": title, "description": description, "status": "queued",
                               "events": ["Tarea creada."]}, self.config(task_id))
            return self.get(task_id)

    def decide(self, task_id, decision, note):
        with self.lock:
            task = self.get(task_id)
            if task["status"] != "proposed" or not task["awaiting_review"]:
                raise ValueError("Esta tarea ya no está pendiente de revisión.")
            self.graph.invoke(Command(resume={"decision": decision, "note": note}), self.config(task_id))
            return self.get(task_id)

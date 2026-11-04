"""Local orchestration and persistence for a single application process.

The SQLite index makes queue and artifact state inspectable; LangGraph checkpoints
preserve the work and human interrupt. This is not a distributed task queue.
"""
import difflib
import json
import os
import re
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command
from app.checks import CHECKS, check_proposal, safe_path
from app.workflow import build_graph

ROOT = Path(__file__).resolve().parent.parent
IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9-]{0,40}$")
ACTIVE = ("executing", "proposed", "amendment-pending")


def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class WorkflowService:
    def __init__(self, directory: Path):
        directory.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.conn = sqlite3.connect(str(directory / "prototype.sqlite3"), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, title TEXT NOT NULL)")
        columns = {row[1] for row in self.conn.execute("PRAGMA table_info(tasks)")}
        for name, declaration in (("contract_json", "TEXT"), ("status", "TEXT NOT NULL DEFAULT 'queued'"),
                                  ("attempt", "INTEGER NOT NULL DEFAULT 0")):
            if name not in columns:
                self.conn.execute(f"ALTER TABLE tasks ADD COLUMN {name} {declaration}")
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS controls (name TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS task_notes (id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL, message TEXT NOT NULL, at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS artifacts (path TEXT PRIMARY KEY, content TEXT NOT NULL, revision INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS promotions (task_id TEXT NOT NULL, attempt INTEGER NOT NULL, path TEXT NOT NULL, content TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY(task_id, attempt, path));
        CREATE TABLE IF NOT EXISTS telemetry (id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL, instance TEXT NOT NULL, attempt INTEGER NOT NULL, at TEXT NOT NULL, outcome TEXT NOT NULL, cost_usd REAL NOT NULL, runtime TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS handoffs (source_id TEXT NOT NULL, target_id TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY(source_id, target_id));
        """)
        telemetry_columns = {row[1] for row in self.conn.execute("PRAGMA table_info(telemetry)")}
        if "cost_known" not in telemetry_columns:
            self.conn.execute("ALTER TABLE telemetry ADD COLUMN cost_known INTEGER NOT NULL DEFAULT 1")
        if "usage_json" not in telemetry_columns:
            self.conn.execute("ALTER TABLE telemetry ADD COLUMN usage_json TEXT")
        if "session_id" not in telemetry_columns:
            self.conn.execute("ALTER TABLE telemetry ADD COLUMN session_id TEXT")
        self.conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS telemetry_session ON telemetry(session_id) WHERE session_id IS NOT NULL")
        self.conn.commit()
        self.graph = build_graph(SqliteSaver(self.conn))
        self._reconcile()

    def close(self):
        self.conn.close()

    @staticmethod
    def config(task_id):
        return {"configurable": {"thread_id": task_id}}

    def _note(self, task_id, message):
        self.conn.execute("INSERT INTO task_notes(task_id,message,at) VALUES (?,?,?)", (task_id, message, utcnow()))
        self.conn.commit()

    def _row(self, task_id):
        row = self.conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if row is None:
            raise KeyError(task_id)
        return row

    def _set_status(self, task_id, status):
        self.conn.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
        self.conn.commit()

    def _snapshot(self, task_id):
        return self.graph.get_state(self.config(task_id))

    def get(self, task_id):
        with self.lock:
            row = self._row(task_id)
            snapshot = self._snapshot(task_id)
            values = dict(snapshot.values)
            legacy = row["contract_json"] is None
            contract = json.loads(row["contract_json"]) if not legacy else {}
            notes = [r[0] for r in self.conn.execute("SELECT message FROM task_notes WHERE task_id=? ORDER BY id", (task_id,))]
            status = values.get("status", "queued") if legacy else row["status"]
            diffs = []
            for path, content in values.get("files", {}).items():
                before = values.get("base_files", {}).get(path, "")
                diffs.extend(difflib.unified_diff(before.splitlines(keepends=True), content.splitlines(keepends=True),
                                                  fromfile="antes/" + path, tofile="propuesta/" + path))
            return {"id": task_id, "title": row["title"], "status": status,
                    "description": values.get("description", contract.get("contract", "")),
                    "contract": contract, "proposal": values.get("proposal", ""),
                    "files": values.get("files", {}), "diff": "".join(diffs), "checks": values.get("checks", {}),
                    "ingestion": values.get("ingestion", {}), "execution": values.get("execution", {}),
                    "blocked_reason": values.get("blocked_reason", ""), "delivery_scope": values.get("delivery_scope", []),
                    "decision": values.get("decision"),
                    "review_note": values.get("review_note", ""), "events": notes + values.get("events", []),
                    "awaiting_review": bool(snapshot.interrupts) and status == "proposed",
                    "legacy": legacy, "attempt": row["attempt"]}

    def list(self):
        with self.lock:
            ids = [row[0] for row in self.conn.execute("SELECT id FROM tasks ORDER BY rowid DESC")]
            return [self.get(task_id) for task_id in ids]

    def artifacts(self):
        with self.lock:
            return [dict(row) for row in self.conn.execute("SELECT path,content,revision FROM artifacts ORDER BY path")]

    def _files(self):
        # The checked-in synthetic pilot instance supplies initial decision records
        # and context. Approved versions in SQLite override those baseline files.
        files = {}
        instance_root = ROOT / "instances"
        if instance_root.is_dir():
            for file in instance_root.rglob("*.md"):
                if file.is_symlink() or not file.is_file():
                    continue
                path = file.relative_to(ROOT).as_posix()
                if safe_path(path):
                    files[path] = file.read_text(encoding="utf-8")
        if self.conn.execute("SELECT 1 FROM sqlite_master WHERE name='apf_instance_files'").fetchone():
            files.update({row["path"]:row["content"] for row in self.conn.execute("SELECT path,content FROM apf_instance_files")})
        files.update({row["path"]: row["content"] for row in self.conn.execute("SELECT path,content FROM artifacts")})
        return files

    def _registry_guard(self, instance):
        try:
            if self.conn.execute("SELECT 1 FROM sqlite_master WHERE name='apf_instances'").fetchone():
                row=self.conn.execute("SELECT * FROM apf_instances WHERE id=?",(instance,)).fetchone()
                if row:
                    config=json.loads(row['config_json'])
                    today=datetime.now(timezone.utc).date().isoformat()
                    if row['status'] not in ('supervised-test','active-demo'):
                        return False, "La instancia no está habilitada."
                    if config['profile']['pilot_end']<today or config['knowledge']['review_date']<today:
                        return False, "La instancia tiene su piloto o revisión vencidos."
                    return True, ""
            registry = json.loads((ROOT / "registry" / "instances.json").read_text(encoding="utf-8"))
            entry = registry.get(instance)
            if not isinstance(entry, dict) or entry.get("status") not in ("active", "pilot", "readiness-test"):
                return False, f"La instancia '{instance}' no está autorizada para ejecutar."
            today = datetime.now(timezone.utc).date().isoformat()
            for name in ("next_review", "pilot_end"):
                if entry.get(name) and entry[name] < today:
                    return False, f"La instancia '{instance}' tiene {name} vencido ({entry[name]})."
            return True, ""
        except (OSError, ValueError, TypeError, KeyError):
            return False, "No se puede comprobar el registro de instancias."

    def _budget_guard(self, instance):
        try:
            cap = float(json.loads((ROOT / "config" / "budget.json").read_text(encoding="utf-8"))["period_cap_usd"])
            if self.conn.execute("SELECT 1 FROM sqlite_master WHERE name='apf_instances'").fetchone():
                instance_row=self.conn.execute("SELECT config_json FROM apf_instances WHERE id=?",(instance,)).fetchone()
                if instance_row: cap=float(json.loads(instance_row[0])['economics']['period_usd'])
            month = utcnow()[:7]
            total, unknown = self.conn.execute("SELECT COALESCE(SUM(cost_usd),0), COALESCE(SUM(CASE WHEN cost_known=0 THEN 1 ELSE 0 END),0) FROM telemetry WHERE instance=? AND substr(at,1,7)=?", (instance, month)).fetchone()
            if unknown:
                return False, "Hay sesiones con coste desconocido: es necesaria una conciliación antes de ejecutar."
            return (total < cap, f"Presupuesto mensual agotado ({total:.2f} de {cap:.2f} USD).")
        except (OSError, KeyError, TypeError, ValueError):
            return False, "No se puede comprobar el presupuesto."

    def is_paused(self):
        with self.lock:
            row = self.conn.execute("SELECT value FROM controls WHERE name='paused'").fetchone()
            return bool(row and row[0] == "1")

    def set_paused(self, paused):
        with self.lock:
            self.conn.execute("INSERT INTO controls(name,value) VALUES ('paused',?) ON CONFLICT(name) DO UPDATE SET value=excluded.value", ("1" if paused else "0",))
            self.conn.commit()
            if not paused:
                self._dispatch_armed()
            return {"paused": self.is_paused()}

    def create(self, title, description, *, instance="readiness-test", series=None, criteria=None,
               invariants=None, scope=None, next_item="END", auto_arm=True):
        with self.lock:
            task_id = uuid.uuid4().hex
            series = series or task_id
            if not IDENTIFIER.fullmatch(instance) or not IDENTIFIER.fullmatch(series):
                raise ValueError("La instancia y la serie deben contener solo minúsculas, números o guiones.")
            scope = [f"instances/{instance}/deliverables/{task_id}.md"] if scope is None else scope
            if not scope or any(not safe_path(p) or not p.startswith(f"instances/{instance}/") for p in scope):
                raise ValueError("El alcance debe contener rutas válidas dentro de la instancia.")
            criteria = criteria if criteria is not None else ["Preparar una propuesta para revisión humana."]
            invariants = invariants or []
            if not criteria or any(not isinstance(x, str) or not x.strip() for x in criteria + invariants):
                raise ValueError("Los criterios no pueden estar vacíos.")
            if next_item != "END" and not re.fullmatch(r"[0-9a-f]{32}", next_item):
                raise ValueError("La siguiente tarea debe ser un identificador válido o END.")
            contract = {"instance": instance, "series": series, "role": "executor", "contract": description,
                        "criteria": criteria, "invariants": invariants, "scope": scope, "next": next_item}
            if self.conn.execute("SELECT 1 FROM sqlite_master WHERE name='apf_instances'").fetchone():
                instance_row=self.conn.execute("SELECT version FROM apf_instances WHERE id=?",(instance,)).fetchone()
                if instance_row: contract['definition_version']=instance_row[0]
            self.conn.execute("INSERT INTO tasks(id,title,contract_json,status) VALUES (?,?,?,?)",
                              (task_id, title, json.dumps(contract, ensure_ascii=False), "queued"))
            self.conn.commit()
            self._note(task_id, "Tarea creada en cola.")
            if auto_arm:
                self.arm(task_id)
            return self.get(task_id)

    def arm(self, task_id):
        with self.lock:
            row = self._row(task_id)
            if row["contract_json"] is None:
                raise ValueError("Esta tarea pertenece a la versión anterior y solo puede consultarse.")
            if row["status"] != "queued":
                raise ValueError("Solo se puede habilitar una tarea en cola.")
            contract = json.loads(row["contract_json"])
            allowed, reason = self._registry_guard(contract["instance"])
            if not allowed:
                self._note(task_id, "Habilitación rechazada: " + reason)
                return self.get(task_id)
            self._set_status(task_id, "armed")
            self._note(task_id, "Tarea habilitada; esperando turno.")
            self._dispatch_armed()
            return self.get(task_id)

    def _series_busy(self, task_id, series):
        rows = self.conn.execute("SELECT id,contract_json FROM tasks WHERE id<>? AND status IN ('executing','proposed','amendment-pending')", (task_id,)).fetchall()
        return any(row["contract_json"] and json.loads(row["contract_json"])["series"] == series for row in rows)

    def _record_session(self, task_id, contract, outcome, execution=None, session_id=None):
        row = self._row(task_id)
        if execution is None:
            execution = {"backend": "unknown", "cost_usd": 0.0,
                         "cost_known": os.environ.get("APF_EXECUTOR", "simulated") == "simulated"}
        self.conn.execute("INSERT OR IGNORE INTO telemetry(task_id,instance,attempt,at,outcome,cost_usd,runtime,cost_known,usage_json,session_id) VALUES (?,?,?,?,?,?,?,?,?,?)",
                          (task_id, contract["instance"], row["attempt"], utcnow(), outcome,
                           execution.get("cost_usd", 0.0), execution.get("backend", "unknown"),
                           int(execution.get("cost_known", False)), json.dumps(execution), session_id))
        self.conn.commit()

    def _recover_session_record(self, task_id, contract, values):
        if values.get("session_id") and values.get("execution"):
            self._record_session(task_id, contract, values.get("status", "unknown"),
                                 values["execution"], values["session_id"])

    def _execute(self, task_id, resume=False):
        row = self._row(task_id)
        contract = json.loads(row["contract_json"])
        self._set_status(task_id, "executing")
        if not resume:
            self.conn.execute("UPDATE tasks SET attempt=attempt+1 WHERE id=?", (task_id,))
            self.conn.commit()
        try:
            previous = self._snapshot(task_id).values
            feedback = previous.get("review_note", "") if previous.get("decision") == "reject" else ""
            input_state = None if resume else {"task_id": task_id, "title": row["title"],
                "description": contract["contract"], "contract": contract, "base_files": self._files(),
                "status": "armed", "decision": "", "feedback": feedback, "events": []}
            self.graph.invoke(input_state, self.config(task_id))
            snapshot = self._snapshot(task_id)
            status = snapshot.values.get("status", "blocked")
            self._record_session(task_id, contract, status, snapshot.values.get("execution"), snapshot.values.get("session_id"))
            self._set_status(task_id, status)
            if status == "blocked":
                self._advance_next(task_id)
        except Exception as exc:
            self._set_status(task_id, "blocked")
            self._note(task_id, f"La ejecución se bloqueó ({type(exc).__name__}).")
            self._record_session(task_id, contract, "error")
            self._advance_next(task_id)

    def _dispatch_armed(self):
        if self.is_paused():
            return
        rows = self.conn.execute("SELECT id,contract_json FROM tasks WHERE status='armed' AND contract_json IS NOT NULL ORDER BY rowid").fetchall()
        for row in rows:
            # A previous execution may already have changed this row.
            if self._row(row["id"])["status"] != "armed":
                continue
            contract = json.loads(row["contract_json"])
            if self._series_busy(row["id"], contract["series"]):
                continue
            allowed, reason = self._registry_guard(contract["instance"])
            if not allowed:
                self._set_status(row["id"], "queued")
                self._note(row["id"], "Habilitación rechazada: " + reason)
                continue
            allowed, reason = self._budget_guard(contract["instance"])
            if not allowed:
                self._note(row["id"], reason)
                continue
            self._execute(row["id"])

    def _promote(self, task_id, values):
        """Idempotent local promotion of the exact approved proposal."""
        attempt = self._row(task_id)["attempt"]
        files, checks = values.get("files", {}), values.get("checks", {})
        if not files or set(checks) != set(CHECKS) or not all(c["passed"] for c in checks.values()):
            raise ValueError("No hay una propuesta aprobada con los cuatro controles verdes.")
        existing = self.conn.execute("SELECT COUNT(*) FROM promotions WHERE task_id=? AND attempt=?", (task_id, attempt)).fetchone()[0]
        if not existing:
            current, base = self._files(), values.get("base_files", {})
            if any(current.get(path) != base.get(path) for path in files):
                raise ValueError("El artefacto cambió antes de completar la integración.")
        with self.conn:
            for path, content in files.items():
                if not safe_path(path):
                    raise ValueError("Ruta de propuesta inválida.")
                inserted = self.conn.execute("INSERT OR IGNORE INTO promotions(task_id,attempt,path,content,at) VALUES (?,?,?,?,?)",
                                             (task_id, attempt, path, content, utcnow())).rowcount
                if inserted:
                    self.conn.execute("INSERT INTO artifacts(path,content,revision) VALUES (?,?,1) ON CONFLICT(path) DO UPDATE SET content=excluded.content, revision=artifacts.revision+1", (path, content))
            self.conn.execute("UPDATE tasks SET status='integrated' WHERE id=?", (task_id,))

    def decide(self, task_id, decision, note):
        with self.lock:
            task = self.get(task_id)
            if task["legacy"]:
                raise ValueError("Esta tarea pertenece a la versión anterior y solo puede consultarse.")
            if task["status"] != "proposed" or not task["awaiting_review"]:
                raise ValueError("Esta tarea ya no está pendiente de revisión.")
            if decision not in ("approve", "reject", "amend"):
                raise ValueError("Decisión desconocida.")
            if decision == "amend" and not note.strip():
                raise ValueError("Indica qué modificación solicitas.")
            if decision == "amend":
                allowed, reason = self._budget_guard(task["contract"]["instance"])
                if not allowed:
                    raise ValueError(reason)
            if decision == "approve":
                if set(task["checks"]) != set(CHECKS) or not all(c["passed"] for c in task["checks"].values()):
                    raise ValueError("No se puede aprobar una propuesta con controles en rojo.")
                snapshot = self._snapshot(task_id).values
                current = self._files()
                if any(current.get(p) != snapshot.get("base_files", {}).get(p) for p in task["files"]):
                    raise ValueError("El artefacto cambió desde la propuesta; recházala y vuelve a ejecutar.")
                try:
                    fresh_checks = check_proposal(current, task["files"], task["delivery_scope"])
                except Exception as exc:
                    raise ValueError("No se pudieron volver a ejecutar los controles; aprobación bloqueada.") from exc
                if not all(c["passed"] for c in fresh_checks.values()):
                    raise ValueError("La propuesta ya no supera los controles sobre el estado actual.")
            if decision == "amend":
                # The resumed graph can initiate a new model session; mark it in
                # flight so startup recovery cannot mistake it for a waiting review.
                self._set_status(task_id, "executing")
            self.graph.invoke(Command(resume={"decision": decision, "note": note}), self.config(task_id))
            values = self._snapshot(task_id).values
            status = values.get("status", "blocked")
            if status == "integrated":
                self._promote(task_id, values)
                self._advance_next(task_id)
            else:
                self._set_status(task_id, status)
                if decision == "amend":
                    self._record_session(task_id, task["contract"], status, values.get("execution"), values.get("session_id"))
            self._dispatch_armed()
            return self.get(task_id)

    def _advance_next(self, task_id):
        row = self._row(task_id)
        if not row["contract_json"]:
            return
        contract = json.loads(row["contract_json"])
        next_item = contract.get("next", "END")
        if next_item == "END":
            return
        if self.conn.execute("SELECT 1 FROM handoffs WHERE source_id=? AND target_id=?", (task_id, next_item)).fetchone():
            return
        try:
            nxt = self._row(next_item)
        except KeyError:
            self._note(task_id, "La siguiente tarea indicada no existe.")
            return
        next_contract = json.loads(nxt["contract_json"] or "{}")
        if next_contract.get("series") != contract["series"]:
            return
        if nxt["status"] == "queued":
            self.arm(next_item)
        if self._row(next_item)["status"] != "queued":
            self.conn.execute("INSERT OR IGNORE INTO handoffs(source_id,target_id,at) VALUES (?,?,?)", (task_id, next_item, utcnow()))
            self.conn.commit()

    def _reconcile(self):
        """Recover interrupted local runs/checkpoints after a single-process restart."""
        with self.lock:
            rows = self.conn.execute("SELECT id,status,contract_json FROM tasks WHERE contract_json IS NOT NULL AND status IN ('armed','executing','proposed') ORDER BY rowid").fetchall()
            for row in rows:
                snapshot = self._snapshot(row["id"])
                values = snapshot.values
                state = values.get("status")
                contract = json.loads(row["contract_json"])
                if state in ("proposed", "blocked", "integrated"):
                    self._recover_session_record(row["id"], contract, values)
                if state == "integrated":
                    try:
                        self._promote(row["id"], values)
                    except ValueError as exc:
                        self._set_status(row["id"], "blocked")
                        self._note(row["id"], f"Recuperación bloqueada: {exc}")
                elif state == "proposed" and snapshot.interrupts:
                    self._set_status(row["id"], "proposed")
                elif state == "blocked" and not snapshot.next:
                    self._set_status(row["id"], "blocked")
                elif row["status"] == "proposed" and state == "queued" and not snapshot.next:
                    self._set_status(row["id"], state)
                elif (row["status"] == "executing" and snapshot.next
                      and values.get("session_backend")
                      and values["session_backend"] != os.environ.get("APF_EXECUTOR", "simulated")):
                    if values["session_backend"] == "openai-compatible" and "generate" in snapshot.next:
                        self._record_session(row["id"], contract, "interrupted",
                            {"backend": "openai-compatible", "cost_usd": 0.0, "cost_known": False},
                            values.get("session_id"))
                    elif values.get("execution"):
                        self._recover_session_record(row["id"], contract, values)
                    self._set_status(row["id"], "blocked")
                    self._note(row["id"], "El ejecutor cambió después de la interrupción; la sesión no se reanuda automáticamente.")
                elif (row["status"] == "executing" and "generate" in snapshot.next
                      and values.get("session_backend") == "openai-compatible"):
                    # A network call might have been processed before the crash. Do
                    # not resend it or invent a cost; pause the instance's budget.
                    self._record_session(row["id"], contract, "interrupted",
                        {"backend": "openai-compatible", "cost_usd": 0.0, "cost_known": False},
                        values.get("session_id"))
                    self._set_status(row["id"], "blocked")
                    self._note(row["id"], "Sesión interrumpida durante una posible llamada al modelo; coste pendiente de conciliación.")
                elif row["status"] == "executing" and snapshot.next and not snapshot.interrupts:
                    self._execute(row["id"], resume=True)
                elif row["status"] == "executing":
                    self._set_status(row["id"], "armed")
            self._dispatch_armed()
            # Recovery of a lost hand-off: a queued successor of a finished item.
            completed = self.conn.execute("SELECT id FROM tasks WHERE status IN ('integrated','blocked') AND contract_json IS NOT NULL ORDER BY rowid").fetchall()
            for row in completed:
                self._advance_next(row["id"])

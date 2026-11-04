#!/usr/bin/env python3
"""Run the executable part of the regression bank (router + deterministic checks).

usage: python3 regression/run.py   (from the repository root)
Exit 0 only if every executable case gives its expected result. Cases marked
pending-runner are counted and listed, not run.
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from route import route  # noqa: E402

bank = json.load(open(os.path.join(ROOT, "regression", "bank-v1.json")))
results, fails = [], 0

# Router
for c in bank["router"]:
    plan = dict(bank["router_plan_expense_L1"], **c.get("plan_override", {}))
    got, why = route(c["case"], plan)
    ok = got == c["expect"]
    fails += not ok
    results.append((c["id"], ok, f"expect {c['expect']} got {got} ({why})"))

# Deterministic checks, on a throwaway repository
DR = "instances/t/decision-records/DR-001-t.md"
DR_TEXT = "# DR-001 — T\n\n- **D1.** The test cap is 25 EUR per case.\n\n---\n\n## Rectifications\n"


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, check=True).stdout.strip()


def scenario(files, delete=(), branch="agent/architect/x", body=""):
    d = tempfile.mkdtemp()
    git(d, "init", "-q")
    git(d, "config", "user.email", "t@t")
    git(d, "config", "user.name", "t")
    os.makedirs(os.path.join(d, "config"))
    os.makedirs(os.path.join(d, os.path.dirname(DR)))
    with open(os.path.join(d, "config", "layers.json"), "w") as f:
        f.write(open(os.path.join(ROOT, "config", "layers.json")).read())
    with open(os.path.join(d, DR), "w") as f:
        f.write(DR_TEXT)
    git(d, "add", "-A")
    git(d, "commit", "-qm", "base")
    base = git(d, "rev-parse", "HEAD")
    for p, text in files.items():
        os.makedirs(os.path.join(d, os.path.dirname(p)), exist_ok=True)
        with open(os.path.join(d, p), "w") as f:
            f.write(text)
    for p in delete:
        os.remove(os.path.join(d, p))
    git(d, "add", "-A")
    git(d, "commit", "-qm", "head")
    head = git(d, "rev-parse", "HEAD")
    bf = os.path.join(d, "body.md")
    open(bf, "w").write(body)
    return d, base, head, branch, bf


SPEC = "instances/t/spec/s.md"
S = {
    "CK-01": ("append-only", dict(files={DR: DR_TEXT + "\n### R·1 — 2026-10-29 — raise\nThe test cap is 30 EUR.\n"})),
    "CK-02": ("append-only", dict(files={DR: DR_TEXT.replace("25 EUR", "40 EUR")})),
    "CK-03": ("append-only", dict(files={}, delete=(DR,))),
    "CK-04": ("citations", dict(files={SPEC: 'Cap: "The test cap is 25 EUR per case" (DR-001, D1).\n'})),
    "CK-05": ("citations", dict(files={SPEC: 'Cap: "The test cap is 99 EUR per case" (DR-001, D1).\n'})),
    "CK-06": ("citations", dict(files={SPEC: 'Cap: "Something that is quoted" (DR-777, D1).\n'})),
    "CK-07": ("layer", dict(files={SPEC: "x\n"}, branch="agent/architect/x")),
    "CK-08": ("layer", dict(files={SPEC: "x\n"}, branch="agent/executor/x")),
    "CK-09": ("layer", dict(files={"config/x.json": "{}\n"}, branch="agent/executor/x")),
    "CK-10": ("scope", dict(files={SPEC: "x\n"}, body="```apf-scope\n" + SPEC + "\n```")),
    "CK-11": ("scope", dict(files={SPEC: "x\n"}, body="```apf-scope\ninstances/t/spec/other.md\n```")),
    "CK-12": ("scope", dict(files={SPEC: "x\n"}, body="no block")),
    "CK-13": ("citations", dict(files={SPEC: 'Límite: «The test cap is 99 EUR per case» (DR-001, D1).\n'})),
}
checker = os.path.join(ROOT, "scripts", "pr_checks.py")
for c in bank["checks"]:
    check, kw = S[c["id"]]
    d, base, head, branch, bf = scenario(**kw)
    r = subprocess.run([sys.executable, checker, check, base, head, branch, bf], cwd=d, capture_output=True, text=True)
    got = "green" if r.returncode == 0 else "red"
    ok = got == c["expect"]
    fails += not ok
    results.append((c["id"], ok, f"{check}: expect {c['expect']} got {got}"))

pending = [r["id"] for r in bank["roles"] if r.get("status") == "pending-runner"]
for cid, ok, msg in results:
    print(("PASS " if ok else "FAIL ") + cid + " · " + msg)
print(f"bank v1: {len(results) - fails}/{len(results)} executable cases pass · {len(pending)} pending a role runner: {', '.join(pending)}")
sys.exit(1 if fails else 0)

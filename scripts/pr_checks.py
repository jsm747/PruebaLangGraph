#!/usr/bin/env python3
"""Deterministic checks on every pull request (tier 1, I.6). Mechanism; no LLM.

usage: pr_checks.py CHECK BASE_SHA HEAD_SHA BRANCH [PR_BODY_FILE]
CHECK = append-only | citations | layer | scope
Exit 0 = green, 1 = red. Prints one line per finding and a final verdict line.

append-only (R11): a decision record (instances/*/decision-records/*.md) is never deleted or renamed, and a
  modified one keeps every byte it had: the old text must be a prefix of the new one, and nothing may be added
  above the `## Rectifications` heading — rectifications are appended inside the record.
citations (R11, Citation Verifier): every quotation of a decision record in a changed markdown file of an instance —
  "<quoted text>" (DR-NNN …) — exists literally in that record as it stands at HEAD.
layer (R12, R10): a branch agent/<role>/… may write only the layers whose writers include that role, and
  never a supervision path (config/layers.json).
scope (R5): an agent branch's PR body declares its scope in a ```apf-scope block (one path per line); the
  files the diff touches must equal that set → scope:match, else scope:mismatch.
"""
import fnmatch
import json
import os
import re
import subprocess
import sys

check, base, head, branch = sys.argv[1:5]
body = open(sys.argv[5], encoding="utf-8").read() if len(sys.argv) > 5 and os.path.exists(sys.argv[5]) else ""


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


def show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


changes = []  # (status, path, newpath)
for line in git("diff", "--name-status", "-M", base, head).splitlines():
    parts = line.split("\t")
    changes.append((parts[0][0], parts[1], parts[2] if len(parts) > 2 else parts[1]))
touched = sorted({p for _, a, b in changes for p in (a, b)})
role = branch.split("/")[1] if branch.startswith("agent/") and branch.count("/") >= 2 else "human"
red = []

DR = "instances/*/decision-records/*.md"

if check == "append-only":
    for st, old, new in changes:
        if not fnmatch.fnmatch(old, DR):
            continue
        if st == "A":
            continue
        if st in ("D", "R"):
            red.append(f"{old}: a decision record may not be deleted or renamed ({st})")
            continue
        before, after = show(base, old), show(head, new)
        if not after.startswith(before):
            red.append(f"{old}: existing text changed; a decision record only grows")
            continue
        added = after[len(before):]
        if "## Rectifications" not in before:
            red.append(f"{old}: no `## Rectifications` section in the closed record")
        elif added.strip() and not re.match(r"### R·\d+ — \d{4}-\d{2}-\d{2} — ", added.lstrip()):
            red.append(f"{old}: appended text must start a dated rectification (`### R·n — YYYY-MM-DD — <title>`)")

elif check == "citations":
    # straight, curly and Spanish angle quotes: a quotation in «…» is checked like one in "…"
    rx = re.compile(r"[\"“«]([^\"”»\n]{8,})[\"”»]\s*\((DR-\d{3})")
    for st, _, new in changes:
        if st == "D" or not new.endswith(".md") or not new.startswith("instances/"):
            continue  # citations are verified inside an instance, against that instance's records
        text = show(head, new) or ""
        for quote, dr in rx.findall(text):
            inst = new.split("/")[1] if new.startswith("instances/") else "*"
            cands = [p for p in git("ls-tree", "-r", "--name-only", head).splitlines()
                     if fnmatch.fnmatch(p, f"instances/{inst}/decision-records/{dr}*.md")]
            src = "".join(show(head, p) or "" for p in cands)
            if not cands:
                red.append(f"{new}: cites {dr}, which does not exist")
            elif quote not in src:
                red.append(f"{new}: \"{quote[:60]}…\" is not in {dr} (not a citation)")

elif check == "layer":
    cfg = json.load(open("config/layers.json"))
    for p in touched:
        if role == "human":
            continue
        if any(p.startswith(s) for s in cfg["supervision_paths"]):
            red.append(f"{p}: supervision path; no agent branch may change what supervises it (role {role})")
            continue
        layer = next((n for n, l in cfg["layers"].items() if any(fnmatch.fnmatch(p, g + "*") for g in l["paths"])), None)
        if layer is None:
            red.append(f"{p}: in no layer of config/layers.json; agents write only inside a layer")
        elif role not in cfg["layers"][layer]["writers"]:
            red.append(f"{p}: layer {layer} is not written by {role}")

elif check == "scope":
    if role == "human":
        print("scope: human branch, no scope declaration required")
    else:
        m = re.search(r"```apf-scope\s*\n(.*?)\n```", body, re.S)
        if not m:
            red.append("no ```apf-scope block in the PR body")
        else:
            declared = sorted({l.strip() for l in m.group(1).splitlines() if l.strip()})
            if declared != touched:
                red.append(f"scope:mismatch — declared {declared}, changed {touched}")
            else:
                print(f"scope:match — {touched}")
else:
    sys.exit(f"unknown check {check}")

for r in red:
    print("RED " + r)
print(f"{check}: {'red' if red else 'green'} · role {role} · files {len(touched)}")
sys.exit(1 if red else 0)

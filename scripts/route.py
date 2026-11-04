#!/usr/bin/env python3
"""Router of a process case (III.3), deterministic, no LLM. Mechanism.

route(case, plan) -> (route, reason)
  route ∈ executor | human | review | auto
Order (III.3; later steps only move a case towards a person, never away):
  1 a deterministic check is red            → executor (no LLM involved)
  2 ceiling L0                              → human
  3 a mandatory-human rule matched          → human (no score lowers it)
  4 exception / classifier abstains         → human
  5 adverse or irreversible decision class  → human, unless ceiling ≥ L1 and a standing approval covers the class
  6 adaptation declared                     → review (adverse/irreversible already went human at 5)
  7 risk high or amount above threshold     → human
  8 risk medium or an assertion in the grey band → review
  9 otherwise                               → auto, under the standing approval
  ceiling L1: auto only for favourable, reversible decisions below threshold (else human)

case: {checks_red: bool, mandatory_human: [ids], exception: bool, abstain: bool,
       decision_class: {adverse: bool, irreversible: bool}, class_id: str, adaptation: bool,
       risk: float, assertions: {id: prob}, amount: float}
plan: {ceiling: "L0"|"L1"|"L2", bands: {low: x, high: y}, threshold: amount,
       assertion_threshold: p, grey_low: q, standing_approvals: [class_id, ...]}
"""
import json
import sys


def route(case, plan):
    if case.get("checks_red"):
        return "executor", "deterministic check red"
    ceiling = plan["ceiling"]
    if ceiling == "L0":
        return "human", "ceiling L0: a person decides every case"
    if case.get("mandatory_human"):
        return "human", "mandatory-human rule " + ",".join(case["mandatory_human"])
    if case.get("exception") or case.get("abstain"):
        return "human", "exception" if case.get("exception") else "classifier abstained"
    dc = case.get("decision_class", {})
    if dc.get("adverse") or dc.get("irreversible"):
        if not (ceiling == "L2" and case.get("class_id") in plan.get("standing_approvals", [])):
            return "human", "adverse or irreversible decision class"
    if case.get("adaptation"):
        return "review", "adaptation declared"
    risk, amount = case.get("risk", 1.0), case.get("amount", 0)
    if risk >= plan["bands"]["high"] or amount > plan["threshold"]:
        return "human", "risk high" if risk >= plan["bands"]["high"] else "amount above threshold"
    grey = [k for k, p in case.get("assertions", {}).items() if plan["grey_low"] <= p < plan["assertion_threshold"]]
    below = [k for k, p in case.get("assertions", {}).items() if p < plan["grey_low"]]
    if below:
        return "human", "assertion below the grey band: " + ",".join(below)
    if risk >= plan["bands"]["low"] or grey:
        return "review", "risk medium" if risk >= plan["bands"]["low"] else "assertion in grey band: " + ",".join(grey)
    if case.get("class_id") not in plan.get("standing_approvals", []):
        return "human", "no standing approval covers this decision class"
    return "auto", "low risk, assertions pass, below threshold, standing approval " + case["class_id"]


if __name__ == "__main__":
    c, p = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    print(json.dumps(dict(zip(("route", "reason"), route(c, p)))))

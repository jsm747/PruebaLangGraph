# Process definition — template

**Filled by:** Architect with the Process Owner and Risk & Control; every change is a project. **Read by:** Executor (derivability), mechanisms (routing), Reviewer, Auditor. **Lifecycle:** normative; versioned; cases pin the version they started with.

---

# <Process> — definition v<n>

**Owner:** <name>  **Risk & Control:** <name>  **Autonomy ceiling:** L0 | L1 | L2 (signed <date>)  **Framework version:** <x.y>

## Purpose and boundaries
<What the process decides or produces; what it never does.>

## Case types
| Type | Entry source | Data fields (R1) | Deliverable per step | Canonical representation |
|---|---|---|---|---|

## State machine of a case
| State | Turn | Leaves when |
|---|---|---|
| received | mechanisms | record created, classified, version pinned |
| armed | Executor | proposal exists |
| checked | mechanisms | checks and classifier materialized |
| routed | — | auto / review / human |
| review | Reviewer | pass or findings |
| waiting:human:gatekeeper | person | approval, override with reason, escalation |
| closed | Integrator | effect executed under approval |
| exception | human | definition does not cover the case |

## Rules of decision
| Id | Frame (operational · normative O/P/F) | Rule (quotable) | Decision class (favourable·adverse / reversible·irreversible / third party) | Derivable inputs | Deliverable |
|---|---|---|---|---|---|

## Mandatory-human rules (step 0, no score lowers them)
| Id | Condition | Route | Reason |
|---|---|---|---|

## Assertable criteria
<One per rule or deliverable; each becomes a question in the question bank.>

## Exceptions policy
<What counts as an exception, who handles it, how it is counted and fed to the process loop.>

## Changes in flight
<Default: open cases finish under their pinned version. Immediate changes (regulatory): pause and re-run.>

## Explanation artefact
<For adverse decisions: the fields the affected person receives — rule applied, facts relied on, who decided, how to contest.>

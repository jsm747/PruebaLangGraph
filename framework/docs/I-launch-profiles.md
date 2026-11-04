# Part I.18 — Launch profiles: pilot and production

The platform and every instance start under one of two profiles. A **pilot** lets an organisation learn on real work before every control is in place, without that becoming a permanent state; **production** is the full framework. Relaxations are a profile, decided once — not a collection of one-off exceptions. As everywhere in the framework, the organisation owns the final choice.

## I.18.1 The two profiles

| | **Pilot** | **Production** |
|---|---|---|
| Duration | Mandatory end date; at expiry the instance is paused automatically | Periodic reviews |
| Scope | One instance (or a few), small volume, named users | As agreed |
| Autonomy | **Ceiling L0 forced**: agents prepare, people decide everything; no external effect without a per-case human approval; no standing approvals | Ceiling from the risk assessment |
| Risk & Control function | May be **deferred**: informed at the start, not asked to sign; a date by which it engages is recorded; the pilot cannot move to production without its signature | Signs ceiling, standing approvals and enterprise policy |
| Enterprise policy | May be a draft | Approved version |
| Platform requirements that may be relaxed | R7 classifier (LLM judge instead); R20 tamper-evident audit (ordinary logs kept); R16 independent liveness (manual monitoring during working hours); R3 a subset of the failure classes (those that apply to the pilot's flows); R17 a single budget cap instead of four levels | As the organisation decides; departures recorded in the adaptation register |
| Signed by | Portfolio Owner (and Framework Owner if a framework rule is relaxed) | Portfolio Owner, Framework Owner, Risk & Control function |

## I.18.2 What the framework recommends never relaxing

The organisation owns its design and may decide otherwise; a departure is recorded once in the adaptation register with the problem it was meant to prevent.


- **Telemetry (R8)** — a pilot that is not measured teaches nothing and cannot justify production.
- **Registry (R21)** — the instance is registered with status *pilot* and its end date.
- **No self-approval** — no agent approves, and none changes what supervises it (R10, R15).
- **Pause** — the queue can be paused at any time by the owner or the Platform Operator.
- **Logs** of every session, decision, approval and effect.
- **Every legal obligation** — data protection, information to workers, sector rules. The framework does not relax law; whether an obligation applies is decided by the organisation's legal function, before the pilot starts.

## I.18.3 Exit from pilot

The pilot records every relaxed or deferred item. The framework recommends closing each before production, together with the Risk & Control function's signature on the ceiling, the standing approvals and the enterprise policy; the organisation decides. A pilot may also end as **no-go**: retired, its lessons filed to the framework queue. A pilot that reaches its end date without either is paused, not extended silently; an extension is a new signature with a new date.

## I.18.4 Where the profile is recorded

Platform: the readiness checklist's profile section. Instance: the instantiation checklist and the registry entry (status *pilot*, end date, deferred items). The orchestrator enforces the pilot's ceiling and end date like any other registry rule.

## I.18.5 Maturity of the framework's own agents

The Builder and the Readiness Agent create and certify everything else, so they start as pilots too. Their maturity is a state of the agent, recorded in the registry, independent of the profile of the instances they create.

| | **Pilot** | **Production** |
|---|---|---|
| Sessions | A **Framework Architect attends every Builder session** as observer and may correct on the spot (for the Readiness Agent: the Platform Operator reviews every draft and test) | The agent works alone with the owner or team |
| Hand-over | Every instance file is reviewed by a person before step 9 (Readiness Agent: every demonstration-log row checked against its evidence by the Platform Operator) | The checklists suffice |
| Scope | A limited number of instantiations set by the Framework Owner; projects and simple processes only — **no complex processes** | All three paths |
| Instances it creates | Always under the pilot profile | The profile that fits |
| Learning | Corrections ledger mandatory; framework review after **each** instantiation | Periodic framework review |
| Exit | Signed by the Framework Owner when criteria fixed **in advance** are met — for example: owner corrections per session under a threshold in the last three sessions; instantiation checklist passing first time above a threshold; no no-go later reversed | — |

The Framework Owner sets the thresholds and the instantiation limit before the first session. A Builder that returns to pilot — after a major framework change to its script, rubrics or templates — follows the same rules.

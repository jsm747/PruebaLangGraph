# Part I.17 — Enterprise registry

Every project, process and agent the organisation runs on this framework is inventoried in one registry. The registry is **a precondition, not documentation**: what is not in it, or is in it with a lapsed review, does not run.

## I.17.1 Three linked inventories

**Instances** (projects and processes) — one entry each:

| Field | Content | Written by |
|---|---|---|
| id, name | stable identifier; human name | Builder (at step 0) |
| purpose | one line | Builder; Architect on definition change |
| shape | project (entry level, current level L0–L4) or process (autonomy ceiling) | Builder; Architect; mechanisms (level changes) |
| status | proposed → instantiating → pilot (with end date) / active → paused / contained → retired | Builder (proposed, instantiating); mechanisms (active, paused, contained); Process Owner (retired) |
| owner · sponsor · Risk & Control contact | directory identities | Builder; changes by Process Owner ruling |
| dates | registered · launched · last review · next review · retired | mechanisms; review dates from the review record |
| framework version | version the instance was built with; current version | Builder; Platform Operator on upgrade |
| enterprise policy version | version the instance was last checked against | Builder; Critic on definition change |
| external effects | kinds, gates, standing approvals with expiry | Builder; Architect on definition change |
| data classes | from the information map | Builder |
| risk and legal | risk assessment and categorisation references; ceiling signature date | Builder; Risk & Control on review |
| budget | period budget and spend to date | Builder; mechanisms |
| indicators | (a), (b), (c) against the baseline; last period | mechanisms (from the ledger) |
| incidents | open incidents and containment state | mechanisms |
| dependencies | instances it consumes from or hands off to; for a process born from a project, *defined-by* that project (and the project lists *defines* the process) | Builder (path 3); Architect |
| path | project · simple process · complex process (defined by <project id>) | Builder |

**Agents** — one entry per agent identity: role, instance, model tier, tool allowlist reference, owner (the instance's Process Owner), created, last review. The framework's own agents (Builder, Readiness Agent) are registered too, with their **maturity** (pilot or production), the framework version they run, the instantiation count and limit, and the exit criteria (I.18.5); their owner is the Framework Owner. Written by the Platform Operator on provisioning; reviewed with the instance. This is the agent registry of R10.

**People in roles** — one entry per binding: person, role, instance, scope, deputy, superior, competence and training date. Derived from each instance's `human-roles-binding`; used to detect orphaned gates and concentration (one person gating many instances).

One writer per field, never per entry.

## I.17.2 Enforcement

Checked by the orchestrator before any agent is armed, and continuously by the liveness monitor:

| Condition | Effect |
|---|---|
| instance not in the registry, or status not *active* | no agent is armed |
| next review date passed | instance degraded to prepare-only (ceiling L0); Process Owner and Portfolio Owner notified |
| owner, deputy or a gate holder no longer in the directory | affected gates escalate to the superior; if the owner is gone, the instance is degraded to prepare-only until an owner is named |
| a standing approval expired | automatic closures under it stop; cases route to humans |
| agent identity not in the registry, or its review lapsed | identity refused at session start |
| telemetry missing for an active instance | flagged; repeated ⇒ paused |
| pilot end date passed without a decision to go to production or retire | paused |
| pilot with a ceiling above L0 or a standing approval | refused (I.18) |

Degradation is the containment ladder's step 2 (I.16.2), applied by the registry instead of by an anomaly.

## I.17.3 Lifecycle duties

- **Builder** — registers the instance as *proposed* at step 0 of the session (even if viability ends in no-go: the no-go is recorded); completes the entry and sets *instantiating* during generation; sets the first review date at handover.
- **Architect** — updates purpose, effects, dependencies and shape when it launches a project, moves a level, or changes a process definition.
- **Mechanisms** — status, dates, indicators, incidents, spend.
- **Process Owner** — confirms the entry at each periodic review; changes of owner; retirement (which revokes the instance's agent identities and archives its records per retention).
- **Platform Operator** — agent entries; framework version on upgrade.

## I.17.4 Portfolio review

A periodic review by the organisation's AI governance function — the **Portfolio Owner** — over what the registry flags by itself: lapsed reviews; instances without owner; expired or expiring standing approvals; ceilings not reviewed; instances without telemetry; people overloaded as gates; instances whose indicators show no improvement over baseline after several periods; open incidents across instances; framework versions behind with lesson-bearing changes pending; instances not yet checked against the current enterprise policy. The Portfolio Owner, with Risk & Control, also amends the enterprise policy (`enterprise-policy`). Outcomes are rulings on instances (continue, change owner, degrade, retire) — not on their content, which stays with each Process Owner.

The Portfolio Owner governs **what is running**; the Framework Owner governs **how instances are built**. They may be the same function; they are different decisions.

## I.17.5 Regulatory use

The registry is the organisation's inventory of AI systems: purpose, owner, risk category, oversight, data, logs and incidents per system, as quality-management and AI-governance standards and high-risk regulation expect. Exports for auditors are views of it, not separate documents.

# Part II — Projects

A project is **finite work with an end state**: a product launch, a process redesign, a report that must exist by a date. It is run as a **chain of closed contracts** that executes on its own and ends with an audit. This part says how a project is designed, planned, executed, audited and closed, which roles act where, and where people decide.

## II.0 Maturity levels

A project does not have to arrive fully defined. It enters at the level its definition supports, and each level is a project whose deliverable is the artefact of the next; the owner holds a gate between levels. A low-definition contract is not a defect at an early level — it is the right contract for that level, and what is verified is the **integrity of the artefact**, not the business outcome.

| Level | Deliverable | Agents | Critic requires | Gate to next |
|---|---|---|---|---|
| **L0 Idea** | a one-page charter: problem, hypothesis, what L1 must answer | Architect with the owner (content door); Distiller over whatever exists | the L1 questions are answerable | owner: worth valuing |
| **L1 Valued** | a quantified business case: model, register of assumptions with sources, sensitivities, risks | Executor builds model and register; Researcher anchors sources; deterministic checks on the model (balances, formulas, units); Reviewer on assumption–model consistency | assumptions anchored or declared unknown; model executable; sensitivities on the critical assumptions | owner (and a financial Gatekeeper above a threshold): invest in planning |
| **L2 Planned** | `project-plan`, closed contracts for the first items, the invariants known so far | Architect in design mode; rolling critique | II.3 | owner: launch |
| **L3 Executing** | the result | the execution loop (II.5) | — | audit |
| **L4 Finished** | the accepted result and **benefits realisation**: what was obtained against the L1 business case | Auditor compares with the total scope and with the L1 valuation; Architect retrospective | — | owner: closure |

A project may enter at any level (it already has a plan: L2) and may **end at any gate** with its artefact as a valid result — an L1 that concludes "no" is a finished project, not a failed one. The gap between L1's valuation and L4's realisation is a series of the ledger and calibrates future valuations.

## II.1 What a project is here

- A **maturity level** it enters at (II.0), and a gate at the end of each level.
- A **chain** of items, each a closed contract (I.4 principle 1), with dependencies and an order.
- A **plan** approved by the Process Owner before anything runs: the chain, the milestones with dates, the people who hold the gates, the budget.
- An **audit** at the end that compares what was delivered with the whole scope and executes the project's invariants.
- **Time** as a first-class fact: milestones have dates, some carry an external commitment, and plan-versus-actual is tracked by the orchestrator, not remembered by anyone.

## II.2 Lifecycle

| Stage | Who | Output | Gate |
|---|---|---|---|
| 1. Design | Architect with the owner and members (content door) | spec, decision records, chain of items, context skill | — |
| 2. Plan | Architect | `project-plan` | — |
| 3. Critique | Critic | approval of the plan and of the first items; every later item is critiqued when it is about to be armed | **fail-closed** on the item being armed: nothing runs in sketch |
| 4. Launch | Process Owner | plan approval; first item armed | **human** |
| 5. Execution loop | Executor, checks, classifier, Reviewer, Integrator, Resolver | one proposal per item, integrated; next item armed | external effects → Gatekeeper |
| 6. Audit | Auditor | audit verdict, ledger, correctives (bounded) or escalation | — |
| 7. Correctives | same loop, one round | corrective items integrated | — |
| 8. Closure | Process Owner | acceptance; promotion of the result; context skill archived; panel consumed | **human** |

The owner approves twice: the plan at launch and the result at closure. In between, the owner is called only by the ladder (I.8) or when a milestone with external commitment must move (II.4).

## II.3 Designing the chain

**Each item is a closed contract**: purpose; assertable acceptance criteria; executable invariants with their pre-execution result; semantic anchors to existing material (never a location that moves); decisions closed, derivable by quotation, or declared free; the structured scope the Executor must declare; a link to the next item, or the end marker that arms the Auditor.

**Partition by default** when any of these holds: the item crosses two areas of responsibility; it has more than about five acceptance criteria; it contains an open design decision; its definition of done is an enumerable list (each element is an item). Sizing optimism is the Architect's most frequent error; the Auditor's proposals-per-item series calibrates it.

**What the Critic checks on a contract.** (1) Every decision is closed, derivable or declared free. (2) Every criterion is assertable. (3) Every invariant declared is executable and has a pre-execution result; an item that declares none says why and which invariants it will produce or which milestone they belong to. (4) Every claim about existing state carries a verified anchor. (5) The scope fits one proposal. (6) The item links to the next or carries the end marker. (7) No external effect without an assigned gate. (8) The gatekeepers named are available when the item is expected to reach them. (9) Nothing in the contract conflicts with the enterprise policy.

**Rolling contracts and growing invariants.** A project does not have to be fully specified at launch. At launch the plan and the first items are closed contracts; later items may be **sketches** — purpose and dependencies — that receive their closed contract, and their critique, just before their turn. The rule is only that no item is armed in sketch. Two devices keep exploration inside the system:
- **Discovery items.** An item whose deliverable is the closed contracts, criteria or invariants of later items is a valid item, with its own assertable criterion: those contracts exist and pass critique.
- **Invariants that grow.** The project declares at launch the invariants it knows, however few, and the plan states **by which milestone the others must exist**. Any item may add invariants as part of its definition of done. The Auditor executes whatever set exists at the end and records as a finding any milestone that passed without the invariants the plan required of it.

**Context skill.** For projects whose design took real deliberation, the Architect writes a context skill at launch — rationale, rejected alternatives, traps, the owner's corrections during design. Non-normative, never quotable, consulted at escalation; archived by the Auditor at closure.

## II.4 The plan

`project-plan` is normative. It contains:
- the chain with dependencies;
- **milestones with dates**, marking which carry an **external commitment** (a customer, a regulator, a public date);
- the human gates, each bound to a person with availability verified against the directory for the window in which the gate is expected;
- the budget of the chain, split by milestone;
- what is measured and when it is reviewed.

**Plan versus actual.** The orchestrator records the expected and actual dates of every item and milestone as facts. The Process Assistant reports slippage to the owner; nobody has to notice it.

**Re-planning.** When a deviation is materialized — an item re-dimensioned by the Resolver, a human SLA expired, a milestone at risk on actual dates — the Architect proposes a re-plan. It is autonomous and goes to the digest, **unless it moves a milestone with external commitment**, in which case the owner approves. No separate planner role: planning and re-planning are the Architect's design mode applied to time.

## II.5 The execution loop

One item at a time per series; the states and whose turn each one is:

| State | Turn | Leaves when |
|---|---|---|
| `armed` | Executor | a proposal with structured scope declaration exists |
| `proposed` | mechanisms | delta computed, scope reconciled, deterministic checks and classifier questions run — all materialized |
| `checked` | Reviewer (if anything is left for it) | verdict materialized: pass, or findings |
| `findings` | Executor | a new proposal addresses them; the convergence rule applies to the Reviewer's next round |
| `approved` | Gatekeeper, only if the item has an external effect | approval fact written |
| `integrated` | Integrator | proposal promoted to current; item closed (complete) or reopened (partial, re-armed); next item armed |
| `blocked` | Resolver | decision published and item re-armed, or escalated up the ladder if the decision has external effect |
| `waiting:human:<role>` | the person | the turn's fact is written, or the SLA escalates |

**Partial delivery.** An Executor that cannot complete the scope in one proposal delivers what is done, declares it partial with a verifiable report of what remains, and the item is reopened and re-armed — capped per round and per item; the cap exhausted sends the item to the Resolver to re-dimension, never to another round.

**Amendments in flight.** People amend through the process door; the orchestrator delivers the amendment at the close of the current turn; nothing is integrated while an amendment is unacknowledged.

**Stalls.** The liveness monitor detects an item with a turn and no activity; deterministic relaunch within caps; then the Resolver; then the ladder.

## II.6 Roles active in a project

| Role | Acts | Does not |
|---|---|---|
| Architect | design, plan, context skill, re-plan, retrospective at closure | execute, approve, arm without the owner's go |
| Critic | the plan and the first items at launch; each later item when it is about to be armed; any re-dimensioned item | execute, rewrite contracts, demand the whole chain closed at launch |
| Executor | one item per proposal | touch other items, approve, restructure |
| Reviewer | every proposal, on what the mechanisms left | chain completeness |
| Resolver | blocked items, re-dimensioning, re-arming | decisions with external effect |
| Auditor | end of chain; one corrective round | legislate, re-audit further |
| Process Assistant | all human turns in and out | decide |
| Distiller | the project's mail, meetings, folders → drafts | arm or write current knowledge |
| Process Owner | plan approval, milestone moves with external commitment, closure, rulings | step-by-step approval |
| Gatekeepers | external effects in their scope | anything outside it |

## II.7 Audit, correctives and closure

The Auditor compares the current state of every deliverable with the total scope of the plan; executes every invariant and records the result; sweeps fidelity to the decision records across the whole result, not proposal by proposal; files a bounded number of corrective items (a short chain, one round) or escalates when a corrective would need design; writes the ledger — cost per actor and per item, review rounds, overrides and escalations, false escalations, proposals-per-item, instrument calibration — and up to a handful of process observations. The audit stays open as the **panel** of what the project left pending until the owner closes it at the next launch.

**Closure** is the owner's acceptance of the result and its promotion to wherever it lives; the Architect's retrospective files the owner's corrections of the design into the user layer; the context skill is archived.

## II.8 Improvement in projects

Level 1: the Auditor's correctives. Level 2: the Process Reviewer reads the project's audit with the others of the instance and queues proposals; the owner rules at the periodic review. Level 3: proposals tagged *framework* go up (I.11). The Architect's retrospective feeds level 4 when the correction was about the Builder or a template.

## II.9 Templates

- `project-spec` — purpose, principles, boundaries, deliverables with canonical representation, assertable criteria, invariants.
- `project-plan` — chain with dependencies; milestones with dates and external commitments; gates bound to people with verified availability; budget by milestone; measures and review dates.
- `work-item` — the contract: purpose, criteria, invariants with pre-execution result, anchors, closed / derivable / free decisions, scope declaration structure, next link or end marker.
- `epic-context` — rationale, rejected alternatives, traps, owner corrections; non-normative; owner; archive at closure.
- `item-checks` — the deterministic checks and classifier questions for an item's deliverable type, with thresholds and the consequence of each failure.
- `project-audit` — total scope comparison, invariant results, fidelity sweep, correctives or escalation, ledger, observations, panel.

# Part I — Common core

What holds for every instance, project or process. Part II covers projects, Part III processes, Part IV how an instance is built.

Vocabulary and invariants everything else depends on. Numbers (caps, timeouts, thresholds, model choices) are calibrations: they are set per instance and tuned by the improvement loop. Everything else in this chapter holds regardless of platform or model.

---

## I.1 What this is

A way of organising AI agents so that they do real work in a business process or project **without a person checking every step, and without losing control**. The work is split into small items with an explicit contract; one agent executes each item; other agents and deterministic checks verify it before it counts; people decide only where a decision is theirs to make — approving something that leaves the company, ruling on how the process should change — and are called in by role, with a deadline and an escalation path. Everything the agents do is recorded as data, so the system can be audited, costed and improved.

**For a project** (a product launch, a process redesign, anything finite): the project is designed up front as a chain of contracts. The chain then runs on its own — execute, verify, integrate, next — and ends with an audit that compares what was delivered with what was promised and files the corrections. The person who owns the project sees the decisions taken on the way and rules on the ones that were escalated.

**For a process** (claims, approvals, recurring operations): each case runs through a fast loop — execute, check mechanically, classify, review only the risky ones — and a person approves only above a threshold. The process definition itself is treated as a project: when the audits or the human overrides show that a rule should change, that change is designed, verified and rolled out through the chain above.

**What it brings.** Autonomy with control: the agents run alone, but nothing counts until it is verified and nothing leaves the company without an approval. Measurability: every session, verdict, override and escalation is data, so cost per unit of delivered work and the quality of each gate are known. Self-improvement: audits produce proposals, a periodic human ruling decides which are executed, and approved changes run through the same machinery. Humans where they matter: by role, with deadlines, with the decision packaged for them, and with escalations counted so that unnecessary ones are removed.

**A starting point.** This framework is a recommended design, not a contract. The organisation that adopts it owns its final design and may keep, change or drop any part; each departure is recorded once, with the problem the original was meant to prevent, in an adaptation register. Repeated adaptations across organisations are the main input for improving the framework itself.

## I.2 The Builder

An instance of this system does not come from a platform team writing workflows. It comes from a **Builder**: an agent that sits with the person who owns the work and turns their task, project or process into a running instance — its contracts, roles, checks, gates, budgets and knowledge — using the templates of Part IV.

**What it does with the owner.** One topic at a time, the owner's frame first, challenge over validation. In order: it tests **viability** (can the owner state what a correct output is in checkable terms, and can each deliverable be represented in a form a tool can compare — if not, the work is not automatable with control and the Builder says so); it settles the **shape** (project or process); it elicits the **spec** and the decision rules as initial decision records; it draws the **permission matrix**, including which actions leave the company and who approves them; it sets the **budget** and records a **baseline** of the current human process; it generates the instance files from the templates; it runs the first execution supervised, with the ledger on.

**What it delivers.** A complete instance: process definition or chain, role annexes, checks and classifier questions, human-role bindings, budgets, ledger schema, knowledge store with the initial records and skills, review cadence with a date. Not a document about the instance — the instance.

**What it never does.** Execute the work itself; approve anything; invent what the owner did not close (an open point becomes an explicit question or an explicit "free"); patch framework templates on its own (I.11).

**How it learns.** Every correction the owner makes during instantiation goes into the Builder's ledger and up the framework queue (I.11), so the next instance starts from a better template. The Builder is itself a role with a mandate, tools, budget and permissions like any other (I.12).

The owner-facing protocol, the viability gate, the minimum viable instance and the templates are in Part IV.

---

## I.3 How it works in one paragraph

Work enters as **items** whose body is a **closed contract**. An **Executor** agent turns one item into one **proposed change**. Deterministic checks, a typed classifier and an adversarial **Reviewer** verify the proposal against the contract; an **Integrator** step promotes it, closes or reopens the item and arms the next one. At the end of a **chain** an **Auditor** compares what was delivered with the total scope, executes the chain's declared invariants and writes the ledger. Stalls are handled by liveness mechanisms; non-derivable decisions by a **Resolver** that decides with published rationale under asynchronous human veto. A **Process Reviewer** reads audits in batches and queues improvement proposals; a human **Process Owner** rules on them periodically; approved proposals execute as ordinary work. Humans sit in the state machine as turns with roles, SLAs and escalation ladders. Everything is observable through **materialized state**: every fact is written by the actor that owns it, into a field, never inferred from prose.

---

## I.4 Principles

1. **Closed contract.** An item leaves nothing to the Executor's invention: every decision is derivable by verbatim quotation from the spec or a decision record, closed at design time, or declared free. Acceptance criteria are assertable; invariants are executable and their pre-execution result is recorded.
2. **Materialized state.** A fact exists only when its owning actor has written it into a field. Nothing is derived from the prose of comments, logs or session output.
3. **One owner per fact; no self-certification.** Each fact has exactly one writer. No actor writes a fact that a gate consumes about its own work.
4. **Turn.** From an item's state follows who must act now. "Nobody's turn" is an anomaly; "someone's turn and they are not running" is a zombie. Humans hold turns too.
5. **Deterministic signatures act immediately; only "still working?" needs an age threshold.** Age thresholds misclassify whenever the failure condition coexists with the condition being detected.
6. **Liveness caps are not cost controls.** Retry and relaunch caps bound lost work; budgets bound spend. Different layers, different owners; neither is weakened to serve the other.
7. **Session output is ephemeral.** Every hand-off is published as a fact or a comment. Nothing lives "in the log".
8. **Mandate, tools, budget and actor guard change together.** A duty without its tool, budget or trigger permission fails at the last step and looks like a design problem.
9. **Rules go where they are followed.** A rule an agent must always follow sits in the header of the artefact it produces, in template form, never as a final procedural step. Declarations are explicit markers or structured fields, never free text matched by pattern.
10. **Citations exist or they are not citations.** Every quotation of a spec or decision record is verified literally by a tool. A paraphrase presented as a quote propagates as truth.
11. **Categorize by nature.** What blocks deterministically is a guard; what is read on demand is a skill; what judges is an LLM role. Choosing the habitual home instead of the right one is a recurring design error.
12. **Memory is not a mechanism.** A duty that depends on a session remembering it becomes a mechanical precondition at its first failure.

---

## I.5 Execution plane

| Concept | Requirement | Fails without it |
|---|---|---|
| **Unit of work** | An item with structured fields: contract, assertable criteria, invariants, state, next-item link, structured scope declaration | The Executor invents what is not closed; everything escalates |
| **Unit of change** | A *proposed* version of the deliverable, separate from the *current* one, with a machine-computed delta and the Executor's structured scope declaration (I.6) | No delta → no adversarial review; no separation → no rollback |
| **Deterministic verification** | Executable checks on the proposal (fields, format, calculations, consistency with sources, checklists), result materialized | Everything is verified by an LLM: expensive and unreliable |
| **Integration** | An atomic step that promotes the proposal to current, closes or reopens the item, and arms the next one | Silent hand-offs; chains stop between items |
| **State** | Fields written by the owning actor, visible on the item — not only inside the engine | Scraping, races, stale state |
| **Events** | Fire on field change with the actor identified; polling only as fallback | Latency, invisible zombies, no actor guard |
| **Turn** | Derivable from state fields alone; includes human turns with role, assignee, SLA and escalation ladder (I.8) | "Nobody's turn" undetected; a waiting human looks like a stall |
| **Agent runtime** | Unattended session with per-role tool allowlist, budget and identity; every hand-off published | Mandate without tool; zombie sessions; lost hand-offs |
| **Knowledge** | Versioned store with immutable history; append-only decisions with a mechanical guard; verifiable citations | Decisions silently rewritten; fabricated citations propagate |
| **Chain** | Next-item link and an end marker that arms the Auditor | Chains neither advance nor get audited |
| **Human gate** | A recorded approval with human identity that no agent can write; agents cannot modify their own supervision | The automation approves itself |
| **Concurrency** | A per-series lock released by a third party if the holder dies | Double arms, collisions, frozen queue |
| **Budget** | Four levels — session, item, chain, period — enforced deterministically; per-session cost telemetry | Unbounded spend; no ledger; no objective function |

---

## I.6 Unit of change: three tiers of verification

Applied in order; each tier handles what the previous one cannot, and costs more than the one before.

**Tier 1 — deterministic.** Every deliverable has a **canonical representation** a tool can compare: structured fields (cell-level diff), extracted plain text (line diff), or the platform's document comparison. The human-facing rendering is a separate artefact. The Executor's **scope declaration is structured** (sections or fields touched, with identifiers), so declared-vs-actual reconciliation is mechanical. Facts produced without any LLM: `delta:computed`, `scope:match` / `scope:mismatch`. A deliverable with no comparable representation cannot be controlled — this is a viability criterion for automating a task (Part IV).

**Tier 2 — typed classifier.** A calibrated decision model (state in; choice, score or boolean-with-probability out) answers **assertions** over current, proposed, delta and criteria. Each assertable criterion and each compliance clause is one question. Outputs become facts only through a **threshold**; the Auditor tracks observed error rates against stated probabilities. Quantitative clauses are *executed*, never asked. Language coverage, context limits and hosting location are instance constraints to check.

**Tier 3 — LLM judge (Reviewer).** Only for what tiers 1–2 did not resolve, and for producing **actionable findings** — a classifier returns verdicts, not the explanation an Executor needs. The Reviewer is adversarial against the contract, clause by clause, and never passes a proposal over a red deterministic result.

**Principle.** *Deterministic where it can be represented; typed classifier where it can be asserted; LLM judge only for the residue and for explanation.* When the platform does not provide a mechanical fact, first represent the artefact so a tool can produce it; add an LLM sensor role only for the residue no representation resolves. In processes (Part III) this ordering is a condition of existence, not an optimization.

---

## I.7 Control plane

| Concept | Requirement | Fails without it |
|---|---|---|
| **Pre-execution critique** (Critic) | A control stage before execution; verdict materialized by the role; fail-closed (I.9) | Defective contracts execute; the cost surfaces at the end |
| **Independent verification** (Reviewer) | Reads proposal, current and contract; writes nothing on the deliverable; its verdict is the only fact the gate accepts | Self-certification |
| **Audit** (Auditor) | Full chain trace plus per-session telemetry (actor, model, tokens, cost, turns, outcome) | No telemetry → no ledger → no objective function |
| **Liveness** | Read state, bounded writes (relaunch, flag), on infrastructure independent of the orchestrator | Silent stalls; an engine outage indistinguishable from idleness |
| **Autonomous decision** (Resolver) | Decisions with rationale recorded in one consultable place; bounded to decisions without external effect | Invisible decisions, or a chain halted on every non-derivable call |
| **Process review** | A proposal queue separate from the work queue; writes limited to marked learning sections | Uncontrolled autonomous improvement, or none |
| **Periodic review** (Process Owner) | Human gate on the *ruling*, not on each execution; approved work runs alone; the queue stops where nothing is ruled | The queue accumulates, or a human sits on every step |
| **Distillation** | A role that reads the raw corpus and writes decision records and skills *in draft state*; a draft is not quotable until a human makes it current | Mail and transcripts as ambient context: no owner, no promotion rule, no minimization |
| **Instrument calibration** | Every instrument (classifier thresholds, sizing, risk scores) measured against outcomes in the ledger | Gameable metrics decide |

---

## I.8 Humans in the state machine

- **Directory.** Person ↔ role ↔ scope ↔ deputy ↔ superior, from the corporate directory.
- **Human turn.** `waiting:human:<role>` assigned to a person, with SLA, reminders and an **escalation ladder** executed by the orchestrator. The top of the ladder stops that item, not the series.
- **What travels up** is a packaged decision — minimal context, options, the Resolver's recommendation with its reasoning trace, side effects, rollback options or "irreversible", cost of delay, and an expiry — not the raw case.
- **Authority is verified.** Role and scope, not "a human". Whoever requested or executed never approves their own work.
- **Escalations are measured, in both directions.** Human intervention per delivered point is disaggregated by role. A **false escalation** — the superior decides as the lower level would have — is counted and is the signal to raise the lower level's autonomy. A **rubber stamp** — a human approval identical to the proposal in near-zero time — is counted too and is the signal of automation bias: the oversight is not happening.
- **Overrides are learning signals with attribution.** Per-person attribution makes this an employee metric; its governance is settled before the ledger is switched on.

**Two doors, no side channels.** People in a project talk to two agents and only two:
- **The process door — the Process Assistant.** Both directions. It holds no privilege of its own: every signal carries a delegated, short-lived token of the person who asked. *Inbound:* status, deadlines, approvals, amendments, pauses, escalations, "where is my item" — it turns what the person asks into **signals** to the orchestrator **with that person's permissions**, never its own. *Outbound:* it is the orchestrator's voice to people — delivers each human turn to its assignee with the packaged decision, reminds before an SLA expires, announces an escalation to the next person on the ladder and informs the previous one, reports blocked items, exhausted budgets and paused queues to the Process Owner, returns the acknowledgement of an amendment, and publishes the periodic summary. The orchestrator decides *when* (SLA, ladder, threshold, budget); the Assistant decides *how and to whom it is said*; it decides nothing else.
- **The content door — the Architect.** What is done, why, scope, criteria, design doubts. It talks to any member, but a decision closes only with whoever holds the authority for it; input from anyone else becomes a draft or an open question. The Architect never reminds or escalates: a process block that surfaces in a content session is filed as a signal through the process door.
- **Nobody talks to the executing agents.** Not the Executor, the Reviewer, the Critic or the Auditor. Any communication about work in flight is an amendment through the process door, delivered by the orchestrator at the close of the current turn; nothing is integrated with an amendment unacknowledged. No instructions off the record, no lost messages.

---

## I.9 Failure mode of a control is a parameter

| Human present to attend a stop | External effect downstream | Default |
|---|---|---|
| yes | any | **fail-closed**: approval required |
| no | yes | **fail-closed**, meaning *up the ladder* (I.8), never a dead stop |
| no | no | **fail-open with trace** |

Containment is graded (I.16.2): freeze a session → degrade a scope to prepare-only (ceiling L0) → pause the scope → quarantine the instance. Fail-closed controls need a **convergence rule** or they loop: from the second round a control may object only to findings that are new or unresolved, never reopening what it accepted; after N non-converging rounds a breaker escalates to a human with the disagreement exposed, not to more rounds.

---

## I.10 Substrate contract

Separate file: [`I-substrate-contract.md`](I-substrate-contract.md).

---

## I.11 Learning across instances

Four levels. The first two live inside an instance; the last two are what makes separate projects and processes learn from each other.

1. **Within a chain.** The Auditor files correctives.
2. **Across chains of one instance.** The Process Reviewer reads audits in batches and queues proposals; the Process Owner rules; approved changes land in the instance's definition or annexes.
3. **Across instances.** Every ruling classifies each proposal by **axis**: *local* (this instance only) or *framework* (templates, generic mandates, the Builder's protocol, the substrate contract). Framework proposals are not executed in the instance: they go to a **framework queue** with its own periodic review, owned by a human **Framework Owner** with a **Framework Architect** (the Builder's own architect). Approved changes land in templates and mandates; new instances are born with them; existing instances adopt them when they move to the new version.
4. **The Builder on itself.** The owner's corrections during instantiation sessions — what was asked badly, what was assumed, which template did not fit — are recorded in the Builder's ledger and enter the framework queue as proposals on its own protocol and templates.

Rules:
- **Organisations' adaptation registers are an input**, alongside proposals: a piece of the framework that several organisations drop or change is a candidate for change.
- **Promotion by recurrence.** A learning seen in one instance stays in its annex; seen in two or more, it is a framework candidate. Never promoted automatically.
- **One writer per layer.** Only the framework review writes the framework layer; an instance cannot patch a template even when it "knows" the improvement.
- **Versioning.** Each instance records the framework version it was born with. A lesson that changes a default (a cap, a threshold) applies **upwards** even where an instance pinned the old value; the release note names the instances affected.
- **Shape tag.** Proposals are also tagged *project* / *process* / *both*; a lesson from processes does not reach project templates without passing the review as *both*.
- **Closure.** Every approved framework proposal ends in a concrete change to a Builder file — template, mandate, checklist. If there is no file to change, it was not a framework proposal.

---

## I.12 Roles · I.13 Knowledge · I.14 Budget governance · I.15 Regulatory hooks · I.16 Security model · I.17 Enterprise registry · I.18 Launch profiles

Separate files: [`I-roles.md`](I-roles.md) · [`I-knowledge.md`](I-knowledge.md) · [`I-budget.md`](I-budget.md) · [`I-regulatory-hooks.md`](I-regulatory-hooks.md) · [`I-security.md`](I-security.md) · [`I-registry.md`](I-registry.md) · [`I-launch-profiles.md`](I-launch-profiles.md).

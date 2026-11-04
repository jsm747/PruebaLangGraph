# Part I.12 — Roles

A role is either an **LLM role** (a session with a mandate), a **human role** (a person bound through the directory), or a **mechanism** (deterministic, no LLM). The separation of powers is structural: the role that designs does not execute, the one that executes does not verify, the one that verifies does not audit completeness, the one that audits does not legislate, the one that proposes improvements does not arm them.

## I.12.1 Role document template

Every LLM role is described with the same twelve fields. The instance adds an annex with the same structure.

1. **Mandate** — what it does, one paragraph. **Never does** — explicit list.
2. **Positional rules** — the rules it must always follow, placed in the header of the artefact it produces, in template form.
3. **Reads / materializes** — data classes it reads; state facts it writes and solely owns. This is its row of the permission matrix (I.12.4).
4. **Tools** — allowlist.
5. **Trigger and actor guard** — on which event it runs, which actors may trigger it, concurrency.
6. **Budget and model tier** — turns, tokens, time per session; model tier with fallback and override.
7. **Reading discipline** — what it reads first, in what order, within what reading budget.
8. **Failure mode** — fail-open or fail-closed by the rule of I.9; caps; convergence rule; breaker and to whom it escalates.
9. **Session output rule** — every hand-off is published as a fact or comment; nothing stays in the session.
10. **Value measurement** — the ledger class it belongs to (productive / sensor / null / redundant / reverted) and the series that measures it. A role without a series can be neither retired nor defended.
11. **Instance annex** — what the instance adds.
12. **Rationale** — one line per non-obvious rule: the problem it prevents.

**Rule:** a change to the mandate revisits tools, budget and actor guard in the same change. A duty without its tool, its budget or its trigger permission fails at the last step and looks like a design problem.

## I.12.2 Catalogue — LLM roles

The generic mandate of each role, in the twelve-field form, is in `roles/`. The blocks below are the catalogue summary.

### Executors

**Builder.** Instantiates the system with the owner (I.2, Part IV). Its own mandate: `roles/builder.md`.

**Architect.** Designs a project as a chain of closed contracts — scope, partition into items, assertable criteria, executable invariants, context for the Executor — and files the design decisions. Never executes, approves, or arms without the owner's go. Strong model tier. Measured by: human corrections per design session; proportion of items that needed re-dimensioning; chain audit findings attributable to design.

**Executor.** Turns one item (or one case) into one proposed change, with a **structured scope declaration**. Delivers partially, with a verifiable report of what remains, when the scope does not fit one proposal. Decides only what is derivable by verbatim quotation; escalates the rest with the question posed. Never restructures the chain, never approves, never touches another item. Model tier by instance; cheapest that passes the gates. Measured by: proposals per item; review rounds per proposal; scope mismatches.

**Researcher** (subagent of the Executor). Read-only: maps the sources an item depends on, verifies that the anchors the contract cites exist, and reports discrepancies and dependencies before execution starts. Never writes.

**Pre-reviewer** (subagent of the Executor). One pass of the proposal against the contract before it is submitted; a bounded number of correctness and scope findings; no style. Prevents the obvious from reaching the Reviewer. Cheap tier.

### Controls

**Critic.** Reviews a **contract** before it is executed — a project item, a project design, a process definition change: is every decision closed, derivable or declared free; are the criteria assertable; are the invariants executable; is the scope one item. Fail-closed: nothing is armed without its approval. From the second round it may object only to findings that are new or unresolved; after N rounds without convergence it escalates to the Process Owner with the disagreement exposed. Strong tier. Measured by: findings that later became audit findings (leaks); rounds per contract.

**Reviewer.** Judges a proposal against its contract, clause by clause, after the deterministic checks and the classifier have run, and only on what they did not resolve. Produces **actionable findings**. Never passes a proposal over a red deterministic result; never reviews chain completeness (the Auditor's job). In processes, runs by sampling or by risk score. Strong tier. Measured by: leak (defects found by the Auditor or by humans that the Reviewer passed) and rework (findings the Executor contested successfully).

**Resolver.** When an item stalls on a non-derivable decision, decides with full published rationale, re-dimensions oversized items, and re-arms — **never for decisions with external effect**, which go up the human ladder. Its decisions go to the digest for asynchronous veto. Strong tier. Measured by: decisions vetoed; items re-escalated after an autonomous recovery with no progress in between (true thrash).

### Meta

**Auditor.** At the end of a chain (projects) or periodically over a sample (processes): compares what was delivered with the total scope; executes the declared invariants and pastes the result; files bounded correctives or escalates; writes the **ledger** (cost per actor, verdicts, overrides, escalations and false escalations, instrument calibration) and process observations. Never legislates; never re-audits beyond one corrective round. Strong tier.

**Process Reviewer.** Reads audits in batches and publishes a bounded number of evidence-backed proposals, classified by axis (local / framework) and shape (project / process / both); edits only the marked learning sections of trainable skills, with revert if the targeted failure does not improve. Never arms anything; never proposes without a measured series. Strong tier.

**Distiller.** The only role that reads the raw corpus — mailboxes, meeting transcripts, shared files. Writes **drafts** into the knowledge layer: decision records the organisation has evidently taken, skills or skill updates, overrides with their stated reasons. A draft is not quotable and no reading discipline loads it until the ratifier the instance names makes it current — the same proposal → current gate the Executor's deliverables pass. Its outputs carry the data classification of their sources. Measured by: drafts made current vs rejected.

### Platform start-up

**Readiness Agent.** Helps prepare the platform before the first instance: drafts the readiness documents, maps R1–R21 to the stack, writes acceptance tests and records their evidence; runs outside the platform it verifies; never ticks a row, signs or makes a document current. Mandate: `roles/readiness-agent.md`.

### Interfaces

**Process Assistant.** The process door for people (I.8), in both directions. *Inbound:* reads state and ledger, explains where things are and why, and turns a person's request into a signal the orchestrator understands — approve, amend, pause, escalate, re-prioritise — sent **with a delegated, short-lived token of that person**; the Assistant holds no privilege of its own. *Outbound:* delivers human turns with the packaged decision, reminds before SLAs expire, communicates escalations up the ladder, reports blocks, exhausted budgets and paused queues to the Process Owner, returns amendment acknowledgements, publishes the periodic summary. The orchestrator decides when; the Assistant decides how and to whom. Never decides anything else, never writes a fact of its own, never contacts an executing agent. Cheap tier. Measured by: turns delivered on time; reminders that avoided an escalation; escalations that arrived without enough context; questions that visible state should have made unnecessary.

## I.12.3 Catalogue — human roles and mechanisms

**Human roles** (bound through the directory; each with scope, deputy, superior):
- **Process Owner** — owns an instance: closes design decisions, rules on proposals at the periodic review, holds the top of its escalation ladder.
- **Gatekeeper** — approves external effects and promotions within a scope; in processes, by threshold. Several per instance, with different scopes.
- **Platform Operator** — the adaptation team: substrate, budgets, permissions, framework versions, telemetry.
- **Framework Owner** — rules on the framework queue (I.11).
- **Risk & Control function** — the specialised team the organisation designates to assess and sign off AI risk (in some organisations risk management, an AI governance office, internal control or legal): signs process ceilings and standing approvals, co-writes the enterprise policy, can lower a ceiling or pause an instance at any time. The framework names the function, not the department.
- **Portfolio Owner** — the organisation's AI governance function: runs the portfolio review over the enterprise registry (I.17.4); with Risk & Control, writes and amends the enterprise policy (I.13.2); rules on instances (continue, change owner, degrade, retire), never on their content.
- **Framework Architect** — maintains templates, generic mandates and the Builder's protocol under the Framework Owner's rulings. The Platform Operator and Framework Architect roles may sit in one team or in several; in every case the **Framework Owner** is someone who does not implement the changes, so that no one rules on their own work.

**Mechanisms** (no LLM):
- **Integrator** — promotes the proposal to current, closes or reopens the item, arms the next one.
- **Liveness Monitor** and **Heartbeat** — stall and zombie detection; the heartbeat on independent infrastructure.
- **Deterministic Checks** — diff, scope reconciliation, field and format checks, calculations, checklists.
- **Typed Classifier** — assertions and compliance questions with thresholds.
- **Budget Controller** — the four levels.
- **Citation Verifier** — every quotation exists literally in its source.

**Optional instrument:** **Sizer** — a cheap pre-execution sizing of items, introduced only when the periodic review finds that the Auditor's sizing is not independent of what was delivered.

## I.12.4 Permission matrix

Mandatory artefact of every instance. Default values below; the instance tightens, never loosens, except by a ruling.

| Role | Reads | Writes state | Writes knowledge | Triggers | External effects |
|---|---|---|---|---|---|
| Architect / Builder | knowledge, state, ledger | design facts | instance layer (spec, records, annexes) | arm first item (after owner's go) | none |
| Executor | item, knowledge, current deliverable | proposal, scope declaration, blocked/escalated | none | none | none |
| Researcher / Pre-reviewer | item, knowledge, sources | findings | none | none | none |
| Critic | contract, knowledge | critique verdict | none | none | none |
| Reviewer | proposal, current, contract, check results | review verdict | none | none | none |
| Resolver | item, knowledge, state, digest | decisions, re-dimensioned items | none | re-arm | none |
| Auditor | full trace, telemetry | audit verdict, ledger | none | correctives | none |
| Process Reviewer | audits, ledger | proposals | learning sections only | none | none |
| Distiller | **raw corpus**, knowledge | draft queue | records and skills **in draft state** (not quotable until ratified) | none | none |
| Process Assistant | state, ledger (in the person's scope) | signals on behalf of the person | none | as the person may | as the person may, by their approval |
| Process Owner | everything in scope | rulings, approvals | ratifies drafts → current | arm after ruling | per scope |
| Gatekeeper | packaged decision | approvals | none | none | **per scope** |
| Platform Operator | telemetry, configuration | budgets, model tiers, allowlists | none | pause, resume | none |
| Framework Owner / Architect | framework queue | framework rulings | **framework layer** | none | none |
| Mechanisms | state, deliverables | their own facts | none | next item, relaunch | none |

Rules: one writer per knowledge layer; no agent writes an approval fact; no agent changes what supervises it; the *external effects* column is empty for every agent by default — any exception is a ruling, scoped and traced.

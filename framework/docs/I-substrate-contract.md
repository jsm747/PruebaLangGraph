# Part I.10 — Substrate contract

What the platform must guarantee for the roles and controls of this framework to exist. The platform team maps each requirement to its stack and **demonstrates** it with the acceptance test given; the implementation is theirs.

**N** = non-negotiable: without it a named role or control cannot exist. **D** = degradable at a stated cost. Each requirement: *guarantee* · *breaks* (what fails without it) · *acceptance* (what is demonstrated).

---

## A. Work and state

**R1 (N) — Typed work items.** A work item is a record with typed fields: contract, assertable criteria, executable invariants with pre-execution result, state, next-item link, end-of-chain marker, structured scope declaration. Prose in addition, never instead.
*Breaks:* Integrator, Auditor, scope reconciliation, Critic.
*Acceptance:* create an item with every field via the platform API, read them back typed, show that an unstructured item cannot be armed.

**R2 (N) — Materialized, visible state.** Every fact about an item is a field written by its owning actor and visible on the item to humans and external watchers, not only inside the engine.
*Breaks:* liveness monitor, human oversight, audit trace.
*Acceptance:* for each fact in the protocol vocabulary, its field, its sole writer, and a human reading it without opening the engine.

**R3 (N) — Orchestrator guarantees.** A durable workflow engine owns each item's state machine and provides: events on field change with actor identity; exactly-once execution of each step; a per-series lock whose release does not depend on the holder being alive; timeouts on every turn; acceptance of external signals (amendment, pause, priority change) without races; an explicit, exportable definition of the state machine.
*Breaks:* all of the mechanics (Part I.14 and Parts II–III); without the lock release the queue freezes on the first dead session; without external signals a human cannot intervene in flight.
*Acceptance:* the failure classes listed in `why.md` are each demonstrated against the engine configuration.

## B. Change and verification

**R4 (N) — Proposal / current separation with history.** Current and proposed versions of every deliverable are kept apart, with immutable version history and rollback.
*Breaks:* Reviewer, Integrator, recovery from a wrong promotion.
*Acceptance:* propose, promote, roll back; an agent identity cannot overwrite the current version except through the Integrator step.

**R5 (N) — Canonical diffable representation.** Every deliverable is stored in a form a deterministic tool can compare (structured fields, extracted text, or the platform's document comparison), alongside its rendering; the delta is computed and persisted.
*Breaks:* deterministic checks, scope reconciliation, Reviewer's clause-by-clause fidelity, Auditor's final-vs-scope comparison.
*Acceptance:* for each deliverable type, compute a delta between two versions and reconcile it mechanically against a structured scope declaration.

**R6 (N) — Deterministic verification hooks.** Executable checks (fields, format, calculations, consistency with sources, checklists, citation existence) run on every proposal; the result is a materialized fact the gate reads.
*Breaks:* tier 1; the Reviewer's "never pass over red verification" rule.
*Acceptance:* register a check, violate it, show the red fact and the refused promotion.

**R7 (D) — Typed decision model.** A calibrated classifier callable from the orchestrator on every proposal, with per-call cost and latency recorded.
*Degradation:* everything assertable goes to the LLM judge, at higher cost per check; sampling rates in flows drop; the instance budget is recomputed.
*Acceptance:* run the instance's question bank against a labelled sample; report calibration per question.

## C. Agent runtime

**R8 (N) — Scoped, budgeted, instrumented sessions.** An unattended session has a per-role tool allowlist, a **per-session identity** (short-lived, scope- and time-bound), caps on turns, tokens and wall time, and **per-session telemetry in the OpenTelemetry GenAI conventions** — agent and operation, model, input and output tokens, tool calls, duration, outcome — written where the Auditor reads it. Cost is **derived** from tokens and a price table kept by the Platform Operator; the runtime is not asked for cost.
*Breaks:* ledger, budget governance, session-based liveness signatures, every improvement loop.
*Acceptance:* a session's telemetry record; a session killed by each cap with the cause materialized.
*Verify first:* whether the chosen runtime emits GenAI telemetry (tokens per call, agent and tool spans). If not, a gateway in front of it must capture it — a prerequisite to everything that measures.

**R9 (N) — Model tier per role, with fallback and override.** The model (and effort, where available) per role is instance configuration, with a declared fallback on provider error and an operator override that needs no redeploy.
*Breaks:* cost routing; incident response when a model or provider degrades.
*Acceptance:* change a role's model by configuration; force a provider error; show the fallback engaged and recorded.

**R10 (N) — Actor guard on every write; policy on every tool call.** Every write carries actor identity and role; the platform distinguishes human, agent and specific role. Agents cannot write human-gate facts and cannot modify what supervises them (budgets, allowlists, state machine, checks). Every tool call is evaluated against the role's policy before it fires (policy-as-code), and refused calls are logged. An agent registry lists every agent identity with purpose, authority surface, owner and review date.
*Breaks:* human gate, separation of powers, attribution.
*Acceptance:* an agent identity attempts an approval fact and a budget edit; both refused and logged.

## D. Knowledge

**R11 (N) — Versioned knowledge with append-only decisions and verifiable citations.** Spec, decision records and skills live in a versioned store with immutable history. Decision records are append-only (rectifications appended inside the record), enforced on write. Any quotation an agent makes can be verified by literal search.
*Breaks:* derivability, the Citation Verifier, the Distiller's promotion path.
*Acceptance:* in-place edit of a closed decision refused; appended rectification accepted; a non-existent quote flagged.

**R12 (N) — One writer per knowledge layer.** Knowledge is partitioned into layers (enterprise policy / framework / user / instance); each layer has exactly one writing role, enforced by the platform.
*Breaks:* containment of errors; the trainable-skill loop.
*Acceptance:* the layer map; cross-layer writes by each role refused except the designated writer.

**R13 (N) — Raw-corpus isolation and data classification.** Mailboxes, transcripts and shared files are readable only by the Distiller's identity; classification (personal, confidential, regulated) is enforced on the sources and on what the Distiller emits; other roles see only its outputs.
*Breaks:* distillation; compliance posture for mail and transcripts; use of external classifiers.
*Acceptance:* an Executor identity cannot read the mailbox; a Distiller output carries its classification label.

## E. Control plane

**R14 (N) — Separate queues.** Work, process proposals and audits (an open panel of what the last chain left pending) are distinct queues. A proposal never enters execution without a ruling; an audit is never closed by the role that wrote it.
*Breaks:* continuous improvement; the periodic review.
*Acceptance:* the three queues; a proposal cannot be armed without a ruling fact.

**R15 (N) — Human approval primitive and decision digest.** An approval is a fact written only by a human identity with the required role and scope, through a primitive agents cannot invoke. Every autonomous decision is recorded in one consultable digest.
*Breaks:* human gate; asynchronous veto; decision reports as posterior gate.
*Acceptance:* agent attempt refused; human without scope refused; human with scope writes the fact with identity; the digest lists every autonomous decision of a sample chain.

**R16 (N) — Independent liveness infrastructure.** A zero-LLM monitor on infrastructure that does not share the orchestrator's failure modes (hosting, billing, credentials) reads state and can revive or flag the orchestrator. Credential liveness is included: a revoked credential escalates on the first tick. The monitor also reads drift signals — unexpected tool-invocation rates, cost-per-task spikes — and can apply the containment ladder (I.16.2).
*Breaks:* detection of the orchestrator's own death.
*Acceptance:* stop the orchestrator; the monitor's flag arrives within its interval through a path independent of the orchestrator.

**R17 (N) — Four-level budgets with spend telemetry.** Budgets at session, item, chain and period level are enforced in the orchestrator; exhausting a level pauses new arms in that scope while in-flight sessions finish; spend is attributable per actor and item.
*Breaks:* cost governance; objective-function term (b); operating the system at all under pay-per-use.
*Acceptance:* a small item budget run to exhaustion; the pause fact, the finished in-flight session, the attributed spend.

**R18 (N) — External effects gated and traced.** Any action with effect outside the system (send, publish, pay, notify a third party, change another system's record) executes only after an approval fact by a role whose scope covers it, and leaves a trace linking effect, approval and item.
*Breaks:* the bound on the Resolver's autonomy; accountability for what the system did in the world.
*Acceptance:* external effect from an agent without approval refused; with approval executed and traced.

**R19 (N) — Human directory and human-turn primitives.** Roles resolve to people through the corporate directory (person ↔ role ↔ scope ↔ deputy ↔ superior). A human turn is assignable to a person, has an SLA with reminders, escalates up the ladder on timeout as a mechanism, and the top of the ladder stops the item, not the series.
*Breaks:* Gatekeepers; fail-closed controls; measurement of escalations.
*Acceptance:* assign a turn, let the SLA expire, show escalation to deputy then superior with the packaged decision attached and each step traced.

---

**R20 (N) — Tamper-evident audit records and an ingestion gateway.** Ledger, telemetry and effect traces are write-once and tamper-evident (signed batches, integrity checks) and can be streamed to the organisation's security monitoring. Raw sources pass through an ingestion gateway that masks personal data and screens for embedded instructions before reaching any agent context.
*Breaks:* audit integrity; the structural defence against content-borne instructions.
*Acceptance:* alter a ledger batch → detected; feed a document with an embedded instruction → masked or flagged before context.

**R21 (N) — Enterprise registry with enforcement.** One registry of instances, agent identities and people in roles (I.17), readable by the orchestrator and the liveness monitor; the orchestrator arms no agent of an instance that is not *active* in it or whose review has lapsed; lapsed reviews, departed owners and expired standing approvals degrade the instance as I.17.2 states.
*Breaks:* the inventory of what runs; accountability per instance; the regulatory inventory of AI systems.
*Acceptance:* arm an agent for an unregistered instance → refused; set a review date in the past → instance degraded to prepare-only and owners notified; remove the owner from the directory → gates escalate and the instance degrades.

## F. Order of verification

R8 (telemetry) and R17 (budgets) first: they decide whether the system can be measured and afforded. Then R3 and R19 (the engine and the humans in it). Then the rest. A requirement is met by demonstration, not by description.

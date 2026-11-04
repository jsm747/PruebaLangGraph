# Part I.16 — Security model

Controls that hold regardless of substrate. The principle: an agent that can be manipulated must not be able to do harm on its own — least privilege, no external effect without a human fact, and structural separation between what reads untrusted content and what acts.

## I.16.1 Threat classes and the control that answers each

| Threat class | Control in the framework |
|---|---|
| **Goal hijack** through content (mail, documents, transcripts, case data) | Content is data, never instruction — enforced by structure, not by prompt: the Distiller has no action tools; the Executor writes proposals only and has no external effects; every proposal passes verification; an **ingestion gateway** masks personal data and screens for embedded instructions before any source reaches an agent's context |
| **Tool misuse** | Per-role tool allowlist **plus policy-as-code**: every tool call is evaluated against the role's policy before it fires, and refused calls are logged; high-impact tools run in isolated execution |
| **Identity and privilege abuse** | **Identity per agent session**, short-lived, scope- and time-bound; no persistent credentials; an **agent registry** (purpose, authority surface, owner, review date) kept current; the Process Assistant holds no privilege of its own — every signal carries a delegated, short-lived token of the person (no confused deputy) |
| **Supply chain** (templates, tools, skills loaded at runtime) | Framework version pinned per instance; tools and skills loaded only from the information map and the registry; a change to any of them is a framework or instance change with its ruling |
| **Unexpected code execution** | Executors that generate or run code do so in a sandbox with no network and no credentials; results enter as a proposal like any other |
| **Memory and context poisoning** | Knowledge enters only as drafts made current by a human (I.13); synced skills change only through reviewed items; context skills are non-normative and archived; every record carries its anchor |
| **Insecure inter-agent communication** | Roles do not talk to each other: they write facts the orchestrator routes; composition (Part V) uses an open protocol with authenticated agents |
| **Cascading failures** | Budgets and caps per scope; **containment ladder** (I.16.2); queue pause per scope, never the whole system by default |
| **Human-agent trust exploitation** | Approval requests carry the proposed action, the reasoning trace, side effects, rollback options and an expiry; rubber stamps are measured; adverse decisions carry an explanation artefact |
| **Rogue agents** (goal drift) | Drift signals in the liveness monitor and the ledger: unexpected tool-invocation rates, cost-per-task spikes, outputs diverging from the contract's scope; a session over its anomaly threshold is frozen for a person |

## I.16.2 Containment ladder

Containment is graded, never only on/off:
1. **Freeze the session** — anomaly in one session; the item's turn goes to a person.
2. **Degrade the scope to prepare-only** — lower the autonomy ceiling to L0 for an item type, a chain or a process: agents prepare, people decide, nothing closes automatically.
3. **Pause the scope** — no new arms; in-flight work finishes.
4. **Quarantine the instance** — read-only for every agent identity; credentials rotated; incident opened.
Each step is a fact with an owner; lifting it is a human signal. A breaker that trips repeatedly on the same scope is a proposal for the process loop.

## I.16.3 Audit integrity

The ledger, telemetry and effect traces are **write-once and tamper-evident** (signed batches, periodic integrity checks), streamed to the organisation's security monitoring, retained per the information map, never below the floor regulation sets. Every consequential action has a decision record: who authorised it, what context the agent had, what it decided, which policy applied, what effect followed.

## I.16.4 Approval request — mandatory content

Proposed action · reasoning trace (quotes and rules applied) · side effects, including on other systems and people · rollback options, or "irreversible" · cost of delay · **expiry** after which the request lapses and the item returns to its previous state.

## I.16.5 Evaluation before release

Every framework release and every instance change to a mandate, a template, a question bank or a threshold runs a **regression bank**: golden cases per role (contracts the Critic must pass or fail, proposals the Reviewer must pass or find, cases the router must send where policy says) with the expected facts. A release with a failing bank does not ship. Instances keep their own bank from audited cases.

# Part III — Processes

A process is **the same work repeated at volume**: claims, approvals, onboarding, recurring reporting. It is run as a **versioned process definition** applied to **cases**. Each case runs through a fast loop that is mostly mechanical; the definition itself changes only through a project (Part II). This part says how cases are routed, where people decide, how the process is audited, and how it learns.

This part is the least proven of the framework: the project shape has operating history behind it, the process shape is derived from it. The first process instance rewrites what does not hold.

## III.1 What a process is here

- A **process definition**: the state machine of a case, the rules of decision, the deliverable of each step with its canonical representation, the assertable criteria, the thresholds. Versioned, with decision records; the normative artefact of the instance.
- **Cases**: small, identical in shape, each a contract made of the definition plus the case data. There is no end: the series is open.
- A **service plan**: the operating agreement with the Process Owner — volumes, SLAs per case type, gate thresholds, sampling rates, budget per period, audit cadence. The thresholds in it are standing human approvals (III.4).
- A **process risk assessment** and its result, the **autonomy ceiling** (III.3), signed by the Process Owner and the Risk & Control function before the first case runs.
- Two loops at two speeds: the **case loop** (seconds to days, mostly without an LLM) and the **process loop** (changes to the definition, run as a project).

## III.1a Normative and operational frames

A process definition holds two kinds of rule, and says which is which:
- the **operational frame** — the steps: how a case is handled, in order;
- the **normative frame** — what must, may and must not happen, whatever the steps: each rule typed **O** (obligation), **P** (permission, with bounds) or **F** (prohibition).

The operational frame is the default path. The normative frame bounds every path, including deviations from the default. Simple processes are mostly operational; complex ones need a normative frame because their cases do not all follow one path. Enterprise policy (I.13.2) is the outermost normative frame.

## III.1b How a process is born

- **Simple process** — defined by the Builder in session with the owner: the rules can be stated now, one team and one approval scope, one system with effects, no High risk dimension, initial ceiling at most L1.
- **Complex process** — any of: the owner cannot state the rules of decision and the exceptions in session (they need analysis of data or cases) · more than one team or approval scope · more than one system with effects · any High dimension in the risk assessment · a target ceiling of L2. It is born from a **project** (Part II) whose deliverable is the process definition, question bank, service plan and tests. The project's audit checks the definition against its invariants; at closure the process instance is registered as *defined-by* that project, and goes through people, service plan and a first supervised run before it is *active*.
- A simple process that later meets a complexity condition (a new approval scope, a target ceiling of L2) is changed through a project like any definition change (III.7).

## III.2 The case loop

| State | Turn | Leaves when |
|---|---|---|
| `received` | mechanisms | case record created from the source (R1); data classified; definition version pinned |
| `armed` | Executor | a proposed decision or deliverable with structured scope exists |
| `checked` | mechanisms | deterministic checks and classifier run; risk score and assertions materialized |
| `routed` | — | one of: `auto`, `review`, `human` (III.3) |
| `review` | Reviewer | pass, or findings back to the Executor |
| `waiting:human:gatekeeper` | the person | approval, override with reason, or SLA escalation |
| `closed` | Integrator | decision made current; effect executed under its approval; next step of the case, or case closed |
| `exception` | human; signal to the process loop | the definition does not cover the case |

An Executor that cannot decide on what is derivable from the definition does not escalate to a Resolver: in a process, a non-derivable decision is an **exception** — it goes to a human, and it is counted.

**Adaptation versus exception.** Where the definition has a normative frame, an Executor may leave the operational path for one case when a permission (P) covers what it does and no prohibition (F) or obligation (O) is breached. It declares an **adaptation** (`adaptation: <P id> — why the default path does not fit`), the case is routed to review, and an adaptation is never allowed for an adverse or irreversible decision class. Adaptation is per case and changes nothing; **evolution** — changing the definition — happens only through the process loop, and repeated adaptations of the same kind are its main input, alongside overrides and exceptions.

## III.3 Routing

Three things decide a case's route, in this order; the later ones can only send a case *towards* a human, never away from one.

**Autonomy ceiling of the process.** Set once, from the process risk assessment — regulatory exposure, financial impact, reversibility of decisions, personal data, who bears an error (customer, third party, internal), reputation — signed by the Process Owner and the Risk & Control function, reviewed at each periodic review, changed only through a definition change:
- *Level 0*: no automatic closure; agents prepare, a person decides every case.
- *Level 1*: automatic closure only for favourable, reversible decisions below threshold.
- *Level 2*: full routing as below.

**Decision class.** Every decision rule in the definition carries a class: favourable or adverse; reversible or irreversible; affecting a third party or not. An **adverse or irreversible** decision goes to a human whatever the risk score, unless the ceiling allows it and a standing approval exists for that specific class.

**Mandatory-human rules.** A deterministic list in the definition, evaluated before the classifier: vulnerable person, legal threat, amount, jurisdiction, data class, denial, and whatever the owner and Risk & Control add. A match sends the case to a human and **no score can lower it**. The classifier may *propose* new rules from the override reasons; it never applies them.

Only then, for what the ceiling, the class and the rules have not already decided, the classifier's output is crossed with the service plan's thresholds:

| Condition | Route |
|---|---|
| any deterministic check red | back to the Executor; no LLM involved |
| adaptation declared | **review**, whatever the risk score; human if the class is adverse or irreversible (adaptation not allowed there) |
| risk low · assertions pass · amount or impact below threshold | **auto**: closed with effect under the standing approval |
| risk medium · or an assertion in the grey band | **review** by the LLM Reviewer; auto-close if it passes |
| risk high · amount or impact above threshold · unforeseen exception · classifier abstains · mandatory-human rule · adverse or irreversible class | **human**: the Gatekeeper of that scope |

**Sampling for calibration.** A random fraction of *auto* cases goes to review anyway, and a smaller fraction to a human. This is what measures whether the classifier and the Reviewer remain trustworthy: without it the system only sees the cases it chose to look at. Rates are in the service plan and are adjusted at the periodic review from the calibration series.

**Exceptions.** A case the definition does not cover always goes to a human, and is a signal: a repeated exception is a missing rule, and the process loop takes it.

**Definition change in flight.** Open cases finish under the version they started with, unless the change is marked *immediate* (regulatory), which pauses them and re-runs them under the new version.

## III.4 Human gates

- **Standing approval.** A case closed *auto* produces an external effect — a payment, a letter, a record in another system. This does not bypass the rule that every external effect is approved by a human: the service plan's thresholds **are** that approval, signed once by the Gatekeeper of the scope, with a validity period, and cited by every automatic closure. Changing a threshold is changing the process definition: a project, with its critique and its owner's approval.
- **Per-case approval.** Above the threshold, or on high risk or exception, the Gatekeeper decides on a packaged case: the proposed decision, the checks and assertions, the risk score and why, the cost of delay. SLA, reminders and ladder as in I.8.
- **Override with reason.** A Gatekeeper who decides differently from the proposal must state why; a case is not closed on an override without a reason. The reason is the main learning signal of the process.
- **Segregation.** The person who entered or handled a case never approves it.
- **Explanation and disclosure.** Every adverse decision produces an **explanation artefact** readable by the affected person — the rule applied, the facts of the case it rests on, who decided — separate from the internal rationale; every effect generated by an agent carries the disclosure of AI involvement the instance configures; people subject to decisions are informed as the instance's legal function requires.

## III.5 Roles active in a process

| Role | Acts | Does not |
|---|---|---|
| Executor | one proposed decision per case step | decide what is not derivable from the definition (→ exception) |
| Mechanisms | checks, classifier, routing, standing approval citation, closure with effect | — |
| Reviewer | routed and sampled cases; actionable findings | every case |
| Gatekeeper | per-case approvals in scope; signs standing approvals | cases outside scope; approving own cases |
| Auditor | periodic, sampled | per case |
| Process Reviewer | batches of periodic audits → proposals | arm anything |
| Distiller | overrides and their reasons; mail and meetings of the process team → drafts | write current knowledge |
| Process Assistant | human turns in and out; SLA reminders; exception and backlog reports | decide |
| Architect | the process loop only: designs every definition change as a project | touch cases |
| Process Owner | service plan, rulings, immediate changes | per-case decisions |

## III.6 Periodic audit

The Auditor runs on a cadence from the service plan over two samples plus the full set of exceptions and overrides:
- a **random stratum**, by route (auto, review, human) and by case type — the only measurement of the classifier itself, since a classifier that chooses what gets audited audits itself;
- a **risk-directed stratum**, selected by a classifier over closed cases: borderline scores, unusual patterns for the case type, high impact, cases whose outcome diverges from similar ones;
- **every** exception and override of the period.
The two rates are separate entries of the service plan and are adjusted at the periodic review. It reports:
- outcome quality per route — were auto-closed cases right, as judged against the sampled human decisions;
- **override rate** and the distribution of reasons;
- **false escalations** — human decisions identical to the proposal after real review — and **rubber stamps** — identical in near-zero time;
- SLA compliance per case type and per human role;
- **calibration** — classifier stated probabilities against observed outcomes, per question **and by group of affected people**; override rates by group; Reviewer leak and rework on the sampled cases;
- cost per case by route and by role, against the budget per period;
- process observations.

Its correctives are not cases: they are **proposals for the definition** (a threshold, a rule, a question in the bank) and go to the process loop. The audit stays open as the period's panel until the owner's review consumes it.

## III.7 The process loop

Every change to the definition — a rule, a threshold, a new case type, a question added to the classifier bank — is a **project** (Part II): designed by the Architect from the audit's and the Distiller's drafts, critiqued, approved by the Process Owner, executed, audited. Small changes make small projects; the machinery is the same. The service plan is versioned with the definition.

## III.8 Improvement in processes

The series that drive it, in order of weight: override reasons; exceptions; repeated adaptations; false escalations; calibration drift; cost per case by route. Level 2 (Process Reviewer, periodic ruling) and level 3 (framework) as in I.11. A process instance's lessons about routing and sampling are the ones most likely to be *process* or *both* at the framework review.

## III.9 Templates

- `process-definition` — the case state machine; rules of decision with identifiers and **decision class** (favourable/adverse, reversible/irreversible, third party); **mandatory-human rules**; deliverable per step with canonical representation; assertable criteria; exceptions policy; version.
- `service-plan` — process risk assessment and autonomy ceiling (signers, review date); volumes; SLAs per case type; gate thresholds with standing approvals (signer, scope, validity); routing bands; sampling rates, random and risk-directed; budget per period; audit cadence.
- `case-record` — case data fields, pinned definition version, route taken, facts of each state, approval or override with reason, effect trace.
- `question-bank` — one classifier question per assertable criterion and compliance clause, with threshold, grey band and consequence; risk-score definition.
- `override-log` — the override, who, reason, case, route, outcome at audit.
- `process-audit` — the periodic report of III.6, with the panel of proposals for the definition.

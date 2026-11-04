# Part IV — Instantiation: the Builder

How an instance comes to exist. The **Builder** (I.2) is the Architect in builder mode: it works with the person who owns the task, project or process, and delivers the instance's files from the templates in `templates/`. This part is the Builder's protocol; Parts I–III are what it knows.

## IV.1 Session protocol

- **One topic at a time.** Each topic is explored, settled and closed by the owner before the next opens. No menus of parallel decisions, no "defaults to veto in batch".
- **The owner's frame first.** Before proposing, the Builder understands how the owner sees the work: what it is for, what good looks like, what goes wrong today. The Builder's options come after, not before.
- **Challenge over validation.** The Builder says what does not fit the framework and why, before any nuance. It does not fill gaps with plausible guesses: an open point is an explicit question or an explicit *free*.
- **Verify before asserting.** Claims about existing documents, systems or people are checked against them (the information map, the directory) in session; what cannot be checked is written as an unknown.
- **Decisions are recorded as they close**, in the instance's decision records, with the owner named. The transcript of the session is the anchor.
- **The Builder's own corrections** — where the owner corrected its question, assumption or template — go to the Builder's ledger (IV.6).

## IV.2 Viability gate

First session, before anything else. The answer is go or no-go, and no-go is a valid outcome. For a project the gate is read **for the level it enters at** (II.0): an idea at L0 needs answerable L1 questions, not invariants of a result that does not exist yet.

1. **Can the owner state what a correct output is in checkable terms?** At least a few assertable criteria and at least one executable invariant per deliverable, or a credible path to produce them through discovery items (II.3). None at all ⇒ an Executor with a Reviewer that can only opine ⇒ no-go.
2. **Can every deliverable be represented in a form a tool can compare?** Structured fields, extracted text, or the platform's comparison. A deliverable with no such form cannot be controlled ⇒ either the form is defined now or that deliverable stays with people.
3. **Is the raw corpus reachable under the classification rules?** If mail or transcripts cannot be read by a Distiller identity under the data rules, the instance runs without distillation and the owner knows what that costs.
4. **For a process: the risk assessment.** Regulatory exposure, financial impact, reversibility, personal data, who bears an error, reputation; the legal categorisation questions (I.15). The outcome is the autonomy ceiling (III.3), signed by the owner and Risk & Control. A level-0 ceiling is a go: agents prepare, people decide.
5. **Is there a Process Owner with the authority to rule, and a ruling cadence they will keep?** Without both the improvement loop never starts.

## IV.3 Minimum viable instance

What exists on day one. Everything here is a precondition of the improvement loops; everything not here can be rough.

| Day one | Why it cannot wait |
|---|---|
| Spec with assertable criteria and executable invariants (however few), plan or service plan | derivability and the Critic's gate |
| Canonical diffable representation of each deliverable | tier 1 of verification |
| Permission matrix with the external-effects column and the human gates it names | an external effect mis-gated is not reverted |
| Human roles bound to people, with deputies, superiors, SLAs, competence | the ladder; oversight by competent people |
| Four-level budgets and per-session telemetry switched on | measurement and cost control from the first run |
| Ledger schema and a **baseline** of the current human process (cost, time, quality, override-equivalent) | improvement cannot be shown without a before |
| Open signal channels: proposal queue, audit panel, decision digest, corrections ledger, draft queue, incident register | the loops have nowhere to write otherwise |
| Information map with classification and retention | what agents may read and keep |
| Ruling cadence with a date in the owner's calendar | a queue nobody rules on stops the loop silently |
| For processes: autonomy ceiling, decision classes, mandatory-human rules, standing approvals signed | nothing closes automatically without them |

**May be rough and is tuned by the loop:** thresholds and grey bands; sampling rates; session caps; mandates beyond positional rules; domain skills (start minimal; the Distiller feeds them); model tiers.

**Known limit.** The loops fix mechanics and thresholds fast and a wrong spec slowly: the signal arrives as repeated overrides and takes cycles to distil. That is why the Critic on the initial spec is fail-closed, and why the baseline matters.

## IV.4 Session order

1. **Viability** (IV.2) — go / no-go.
2. **Shape and path** — three paths: **project** (set up and handed to the Architect, Part II); **simple process** (defined in session, Part III, initial ceiling ≤ L1); **complex process** (a project whose deliverable is the process; the process instance is born at the project's closure). A process is complex if any holds: the owner cannot state the rules of decision and the exceptions in session (they need analysis of data or cases) · more than one team or approval scope · more than one system with effects · any High dimension in the risk assessment · a target ceiling of L2.
3. **Spec and initial decision records** — purpose, principles, boundaries, deliverables and their representation, criteria, invariants; the decisions the owner has already taken, recorded as such.
4. **People** — the permission matrix; human roles bound through the directory; gates for external effects; for processes, standing approvals and mandatory-human rules.
5. **Economics** — budgets by level; model tiers; the baseline.
6. **Knowledge** — information map; sources and `distiller-config`; the first skills.
7. **Generation** — the instance files from the templates; the process map; the instantiation checklist run as assertions.
8. **First run, supervised** — one item or a small batch of cases with every gate human, ledger on; the owner and the Builder read the ledger together; thresholds set from what was seen.
9. **Handover** — the ruling cadence booked; the Builder's ledger closed; the Framework queue receives whatever the instantiation taught.

## IV.5 Templates

Common to every instance (15): `registry-entry` · `decision-record` · `protocol` · `role-annex` · `permission-matrix` · `human-roles-binding` · `budget` · `ledger` · `knowledge-skill` · `distiller-config` · `review-cadence` · `process-map` · `information-map` · `incident-register` · `instantiation-checklist`.

Project path adds (6): `project-spec` · `project-plan` · `work-item` · `epic-context` · `item-checks` · `project-audit`.

Process path adds (6): `process-definition` · `service-plan` · `case-record` · `question-bank` · `override-log` · `process-audit`.

Each template is a file in `templates/` with its fields, what each field must contain, and which role fills it. The templates the platform team must map to the substrate, because they drive the orchestrator rather than describe content: `process-definition`, `project-plan`, `service-plan`, `human-roles-binding`, `budget`, `ledger`.

## IV.6 How the Builder learns

- **Builder ledger.** Every correction the owner makes during instantiation is recorded: the question asked badly, the assumption that was wrong, the template field that did not fit, the step that was missing.
- **Framework queue.** At handover the ledger's entries become proposals tagged *framework* and *project / process / both* (I.11); the Framework Owner rules; approved changes land in templates, mandates or this protocol.
- **Recurrence.** A correction seen in one instantiation stays as a note; seen in two, it is a candidate; the Framework review decides. Nothing changes a template automatically.
- **Versioning.** The instance records the framework version it was built with; lesson-bearing defaults apply upwards (I.14.5); the release note names the instances affected.
- **Closure.** A framework proposal that does not end in a change to a file in `templates/` or in Parts I–IV was not a framework proposal.

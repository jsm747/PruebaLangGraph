# Release notes

## v0.4.1 — 2026-10-24
Readiness Agent consistent with the adviser model: its skill starts with a scoping phase in which the team keeps, changes or drops parts of the checklist; the order of work is a suggestion; phase 10 is the team's go-live decision. The agent loads the whole framework as context and, for each adaptation, lists the other parts of the framework that depend on the piece changed; the adaptation register gets an "also affects" column.
Defaults moved: none. Instances affected: none.

## v0.4 — 2026-10-24
Adds I.18 **Launch profiles**: pilot (end date, small scope, ceiling L0 forced, no standing approvals, deferrable items marked (P) in the readiness checklist, Risk & Control function deferrable to a date) and production; items never relaxed (telemetry, registry, no self-approval, pause, logs, legal obligations); exit from pilot; registry status *pilot* enforced. Renames the team-sense "compliance" to the **Risk & Control function** — the specialised team each organisation designates — across the framework.
Also: I.18.5 **maturity of the framework's own agents** — the Builder and the Readiness Agent start in pilot (attended sessions, human review before handover, no complex processes, every instance a pilot, framework review after each instantiation) and move to production when the Framework Owner signs against criteria fixed in advance.
Also: `docs/readiness-guide.md`, a plain-language guide to getting the platform ready with the Readiness Agent.
Changed: **the framework is a starting point; the organisation owns its final design.** The Readiness Agent becomes an adviser — it says once what a recommendation prevents, records the departure in the new `adaptation-register`, and adapts; it does not block, insist or ask for signatures on design choices. The readiness checklist and I.18's "never relaxed" items become recommendations; go-live is the team's decision. Adaptation registers feed framework improvement.
Removed: time estimates, cost multipliers, typical retention figures and other quantitative claims not backed by data; the pre/post sizing agreement threshold is now set at the periodic review.
Defaults moved: none. Instances affected: none.

## v0.3 — 2026-10-24
Adds, from a review of the state of the art: an **enterprise policy layer** (organisation-wide prohibitions, obligations and permissions; written by Risk & Control with the Portfolio Owner; prevails over every instance; template `enterprise-policy`; Critic check 9; Builder loads it first; registry records the policy version); rules typed **O/P/F** and the distinction between **normative and operational frames** (III.1a); **adaptation** per case under a permission, always reviewed and never for adverse or irreversible decisions, versus **evolution** of the definition through the process loop; non-normative **platform notes for Microsoft 365** (BPMN for process definitions, Agent 365 and Entra Agent ID for registry and identity).
Also: the **Readiness Agent** (mandate, operating skill, acceptance test catalogue for R1–R21 with suggested M365 implementations); templates `platform-readiness-checklist` and `demonstration-log`; `docs/platform-guide.md` for those who run the platform and keep the Builder, organised by job (Platform Operator, Framework Architect; the Framework Owner never implements what it rules on); the Builder guide covers risk, compliance and controls (policy check, ceilings, what always goes to a person, controls, overseer duties, transparency, data, incidents).
Defaults moved: none. Instances affected: none.

## v0.2 — 2026-10-24
Adds I.17 Enterprise registry: inventories of instances, agent identities and people in roles; per-field writers; enforcement by the orchestrator (unregistered or lapsed review ⇒ not armed or degraded to prepare-only); Builder registers at step 0 and completes at handover; Architect keeps entries current; Portfolio Owner and portfolio review; substrate requirement R21; template `registry-entry`; regulatory inventory hook.
Also: the Builder's three paths — project, simple process defined in session, complex process born from a project — with the complexity criterion (SKILL step 2, IV, III.1b, registry, checklist); `docs/builder-guide.md`, a plain-language guide for the person who works with the Builder.
Defaults moved: none. Instances affected: none.

## v0.1.1 — 2026-10-21
Adds, on top of v0.1: I.16 Security model (threat classes → controls, containment ladder, audit integrity, approval-request content, regression bank); substrate contract R8 moved to OpenTelemetry GenAI telemetry with cost derived from tokens, R10 per-session identity and policy-as-code, R20 tamper-evident audit and ingestion gateway; Process Assistant without privilege of its own; A2A/MCP alignment in the protocol template; infographic with the Builder band; executive summary and PDF; VERSION as single source; the Architect's internal log moved to `.architect/`.
Defaults moved: none. Instances affected: none (no instance exists yet).

## v0.1 — 2026-10-21
First complete draft: Parts I–IV, 26 templates, 12 role mandates, 6 skills and the operator slot, Builder package (SKILL, rubrics, substrate binding, two examples), one-page infographic, summary. Part V deferred. Budget governance marked draft; the process shape marked as derived.
Defaults moved: none (first release). Instances affected: none.

# Executive summary

**Agent Process Framework** — a substrate- and model-agnostic specification for running business projects and processes with autonomous AI agents, under control. Version 0.4.1, October 2026. One-page map: [`diagrams/system-infographic.svg`](diagrams/system-infographic.svg). Guide to getting the platform ready with the Readiness Agent: [`readiness-guide.md`](readiness-guide.md). Guide for those who run the platform and keep the Builder: [`platform-guide.md`](platform-guide.md). Guide for the person who works with the Builder: [`builder-guide.md`](builder-guide.md). PDF of this summary with the map: [`summary/agent-process-framework-summary.pdf`](summary/agent-process-framework-summary.pdf).

## Objective

Give a large organisation a complete, buildable description of a system in which AI agents carry out real work — a product launch, a process redesign, a recurring operation such as claims or expense handling — **without a person checking every step and without losing control**. It is written for two readers: a **builder agent** that sets up an instance together with the person who owns the work, and the **platform team** that adapts it to the corporate stack (Microsoft 365 or equivalent). It prescribes guarantees and roles, never a product.

## How it works, in short

Work is split into items with an explicit, checkable contract. One agent executes each item; deterministic checks, a typed classifier and an adversarial reviewer verify it before it counts; an integrator promotes it and arms the next. A critic gates contracts before execution; an auditor closes each chain or audits each period. Every fact — verified, reviewed, approved, blocked — is written as data by the role that owns it, never inferred from prose. People sit in the state machine as turns with roles, deadlines and escalation ladders, and talk to the system through two doors only: a process assistant for status and approvals, an architect for content. Nothing with external effect happens without a human approval, standing or per case.

## Value

- **Autonomy with control.** Agents run alone; nothing counts until verified; nothing leaves the company unapproved; every adverse or irreversible decision reaches a person whatever any score says.
- **Measurability.** Every session, verdict, override and escalation is data: cost per unit of delivered work, quality of each gate, calibration of each instrument, human time by role — against a baseline recorded before the first run.
- **Self-improvement.** Audits produce proposals; a periodic human ruling decides; approved changes run through the same machinery; lessons seen in two instances reach the templates every future instance is born from.
- **Humans where they matter.** By role, with the decision packaged, with deadlines and ladders, with false escalations and rubber stamps both counted so oversight is neither a bottleneck nor a formality.
- **Compliance by construction.** Competent oversight, log retention, explanation for adverse decisions, incident handling, data minimisation and the "content is data, never instruction" rule are hooks of the design, not afterthoughts.
- **Start small.** A pilot profile with an end date, ceiling L0 and a short list of deferred controls lets an organisation learn on real work before every control is in place — without that becoming permanent.
- **Fast start.** A builder agent, a day-one checklist, 28 templates, 12 role mandates, operating skills and two worked examples: an instance starts rough where it can and strict where it must.

## What v0.1 contains

- **Part I — common core:** principles; execution and control planes; three verification tiers; humans in the state machine; a 19-point substrate contract the platform must demonstrate; roles and permission matrix; knowledge (five document classes, sources, distillation); budget governance; regulatory hooks; security model; an **enterprise policy** layer every instance inherits; an **enterprise registry** of every instance, agent and person in a role — enforced, so what is not registered or not reviewed does not run; learning across instances.
- **Part II — projects:** maturity levels L0–L4; rolling critique; plan with dates and gates; the execution loop as states and turns.
- **Part III — processes:** autonomy ceiling; decision classes; mandatory-human rules; routing; standing approvals; sampled audit in two strata.
- **Part IV — the Builder:** viability gate; minimum viable instance; session script with questions; rubrics; substrate binding.
- Templates (26), role mandates (12), skills (6 + the operator's slot), two worked examples, the one-page map, the *why* of every principle.

## What is deliberately open

Budget policies (no operating evidence under pay-per-use yet). The process shape is derived from the project shape and will be rewritten by the first real process. Composition of several instances (Part V) waits for a composed instance. The platform team must first verify what cost and session telemetry the chosen runtime exposes — everything that measures depends on it.

# Platform guide — for those who run the platform and keep the Builder

Three jobs keep the system alive: running the substrate the agents live on, maintaining the framework and the Builder, and making the Builder better with every instance. They may sit in one team or in several — an infrastructure team for the first, an AI or process-excellence team for the other two, for example. This guide is organised by job, not by team: whoever holds a job reads its sections.

## 1. Three jobs, and the one none of them holds

| Job | Framework role | What it means |
|---|---|---|
| Run the substrate | **Platform Operator** | Make the guarantees of the substrate contract true and keep them true: orchestrator, identities, telemetry, budgets, liveness, containment, incidents |
| Keep the framework and the Builder | **Framework Architect** | Templates, role mandates, skills, rubrics, the Builder's script and examples; releases |
| Make the Builder learn | **Framework Architect** | Turn what instances and instantiations teach into proposals, and approved proposals into file changes |
| **Rule on framework changes** | **Framework Owner** | A person who does not implement the changes (often the Portfolio Owner) decides which proposals are executed. Whoever implements does not approve their own changes, however the jobs are split |

None of these jobs decides the content of an instance (that is its Process Owner) or the enterprise policy (Risk & Control with the Portfolio Owner).

## 2. Before the first instance

A **Readiness Agent** (`roles/readiness-agent.md`, `readiness/`; plain-language guide: `docs/readiness-guide.md`) works for you through it: it drafts the documents, maps each requirement to your stack, writes the tests (`readiness/test-catalogue.md`) and records what they show. It advises; you decide. When you depart from a recommendation it says once what it was meant to prevent, records it, and adapts.

**Pilot or production.** The checklist starts with the profile (I.18): a pilot defers the rows marked (P) — classifier, tamper-evident audit, independent liveness, part of the failure-class suite, the four budget levels, an approved enterprise policy, the Risk & Control signature — but never telemetry, the registry, the pause, the logs or any legal obligation; it has an end date and runs every instance at ceiling L0.

Everything below is in one checklist, **`templates/platform-readiness-checklist.md`**. It is a **starting point**: the team responsible for the platform owns the final design and decides what to keep, change or drop; departures go once to the `adaptation-register`. It has four parts:

**A. People named** — Platform Operator, Framework Architect, Framework Owner (who does not implement), Portfolio Owner, and the Risk & Control, legal, data-protection and security contacts; an owner for every hand-off between teams.

**B. Documents that must exist**

| Document | Owner |
|---|---|
| Enterprise policy | Risk & Control + Portfolio Owner |
| Substrate binding · substrate operations skill | Platform Operator |
| Demonstration log (R1–R21, template `demonstration-log`) | Platform Operator |
| Price table · model tier defaults · budget defaults | Platform Operator (+ Framework Architect, Portfolio Owner) |
| Retention schedule · raw-corpus classification rules | Data protection + Risk & Control |
| Disclosure wording · explanation template | Risk & Control + legal |
| Workers' information pack · DPIA/FRIA template and trigger | HR, data protection, legal |
| Runbooks: agent identity · containment · incidents | Platform Operator + security (+ legal for incidents) |
| Release procedure · regression bank | Framework Architect |
| Framework and portfolio review calendars | Framework Owner + Portfolio Owner |

**C. Platform demonstrated**, in this order — measurement first (R8 telemetry with the price table, R17 budgets), then engine and people (R3 with the failure classes of `docs/why.md`, R19), then the rest of R1–R21, each with its test and evidence in the demonstration log.

**D. Dry run** — a small real task with a friendly owner, Builder steps 0–7, a first supervised run with every gate human, registry entry active, Builder corrections filed, regression bank extended.

## 3. The routine (Platform Operator unless stated)

| When | What |
|---|---|
| **Continuously** | Liveness and heartbeat healthy; drift signals (unexpected tool calls, cost-per-task spikes) watched; containment applied when they fire (freeze → prepare-only → pause → quarantine); incidents registered and reported as legal has set up |
| **On each new instance** | Provision agent identities (per session, short-lived) and register them; set budgets and model tiers from the instance's `budget`; check the instantiation checklist's substrate items |
| **On each retirement** | Revoke the instance's agent identities; archive its records per retention |
| **Weekly** | Telemetry gaps; spend against budgets per instance; model and provider errors and fallbacks engaged; agents nearing review |
| **Monthly** | Framework review with the Framework Owner (section 5, Framework Architect); registry flags for the portfolio review |
| **On each model or provider change** | One variable at a time; a falsifiable criterion stated before the change; regression bank run; roll back by configuration if the criterion fails |
| **On each release** | Section 4 |

## 4. Maintaining the Builder and the framework (Framework Architect)

**What the Builder is made of:** its mandate (`roles/builder.md`), its start-up package (`builder/SKILL.md`, rubrics, binding, examples), the templates, the role mandates and skills it instantiates, and Parts I–IV, which it reads as knowledge. Changing any of these changes the Builder.

**Rules for any change:**
- It comes from a ruled proposal, never from a single complaint or a hunch.
- A change to a role's mandate revisits its tools, budget and trigger permissions in the same change.
- Rules an agent must always follow go in the header of what it produces, in template form.
- Never loosen the enterprise policy, never weaken liveness caps to save cost, never let an agent edit what supervises it.
- The infographic, executive summary and process maps are updated in the same change as what they depict.

**Release process:** regression bank green → change `VERSION` → regenerate the infographic and the summary → release note (what changed; which defaults moved and in which direction; which instances are affected) → tag on `main`. Instances record the version they were built with; lesson-bearing defaults apply upwards to all of them; others adopt a new version at their next review, checked by re-running their instantiation checklist.

## 4b. The Builder's own pilot (Framework Architect)

The Builder starts in pilot (I.18.5): a Framework Architect attends every session, reviews the instance files before handover, and keeps the corrections ledger; no complex processes; every instance it creates is a pilot. Plan the attendance: it is where the Builder learns. The Framework Owner sets the instantiation limit and the exit criteria before the first session and signs the move to production. The Readiness Agent follows the same rule with the Platform Operator.

## 5. How the Builder learns (Framework Architect, ruled by the Framework Owner)

**Inputs** — four channels, all landing in one **framework queue**:
1. **The Builder's ledger** from every instantiation: each correction the owner made — a badly asked question, a wrong assumption, a template field that did not fit, a missing or superfluous step — with the step of the script where it happened.
2. **Framework-axis proposals** from instances: each instance's Process Reviewer tags proposals *local* or *framework*; framework ones come to the framework queue.
3. **Incidents** whose countermeasure belongs in a template, mandate or the substrate rather than in one instance.
4. **Portfolio review findings**: patterns across instances (reviews always lapsing in one kind of instance, instances that never beat their baseline, ceilings that never move).

**The framework review** (monthly, chaired by the Framework Owner, prepared by the Framework Architect):
- Every proposal gets a ruling: approved (with position), merged into another, closed. Nothing is deferred.
- **Recurrence decides**: a correction seen once is noted; seen in two instantiations or instances, it is proposed; the Framework Owner decides.
- Each approved proposal names the file it changes, the series that will show the effect, and a criterion with a date. If no file changes, it was not a framework proposal.
- Proposals are tagged *project / process / both*: a lesson from processes does not change project templates unless ruled *both*.

**Measure the Builder** — these are its series; report them at each review:
| Series | Direction |
|---|---|
| Owner corrections per instantiation session | falling |
| Instantiation checklist items passing first time | rising |
| Time from first session to first supervised run | falling |
| Instances still active and reviewed after three periods | rising |
| No-go decisions later reversed (a viable task rejected) or regretted (a go that should have been a no-go) | falling |
| Regression bank size and pass rate | rising / 100 % |

**Grow the regression bank**: every audited instance contributes cases whose outcome is known — a contract the Critic should have stopped, a proposal the Reviewer should have found, a case the router sent to the wrong place. A change to the Builder that breaks an old case does not ship.

## 6. What to watch for

- **Implementers approving themselves.** If the Framework Owner seat is empty or held by whoever implements, proposals turn into whatever is convenient to implement. Escalate it to the Portfolio Owner.
- **Jobs falling between teams.** When the jobs sit in different teams, the hand-offs are where things are lost: a framework release the platform does not deploy, a telemetry gap nobody reports to the Framework Architect, a model change made without re-running the bank. Name an owner for each hand-off.
- **Template drift.** Instances patching their own copies of templates "because it was faster". Instances extend through annexes; templates change only through the framework queue.
- **Silent telemetry loss.** Everything that measures — ledger, objective function, Builder series — depends on R8. An instance without telemetry is flagged, then paused.
- **Budget creep hidden as liveness.** A request to raise retries or caps "so it doesn't stall" that is really about getting more out of a contested item: that is a contract problem, not a cap problem.
- **Orphans.** Owners who leave; gates bound to people who moved. The registry flags them; act on the flag.

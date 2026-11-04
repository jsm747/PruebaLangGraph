# Platform readiness checklist — template

**Filled by:** the team responsible for the platform (Platform Operator, Framework Architect); go-live decided by that team. **Read by:** the first Builder, Risk & Control, auditors. **Lifecycle:** a **starting point**. The team responsible for the platform owns the final design: it keeps, changes or drops rows as it sees fit; departures from the framework's recommendation go to the `adaptation-register`, once, with the problem they were meant to prevent. Re-used after major platform changes if the team wishes.

---

# Platform readiness — <organisation> — framework <x.y.z>

## Profile (I.18)
☐ **Pilot** — end date <date> · scope <instances, volume, users> · ceiling L0 forced · Risk & Control function deferred until <date> or engaged
☐ **Production**

Rows marked **(P)** are the framework's suggestion of what a pilot can defer. The team decides.

## A. People named

| ☐ | Role | Person | Deputy | Confirmed on |
|---|---|---|---|---|
| ☐ | Platform Operator (lead) | | | |
| ☐ | Framework Architect (lead) | | | |
| ☐ | Framework Owner — does not implement framework changes | | | |
| ☐ | Portfolio Owner (AI governance function) | | | |
| ☐ | Risk & Control contact (P: may be deferred to a date) | | | |
| ☐ | Legal contact (categorisation, reporting duties) | | | |
| ☐ | Data protection contact | | | |
| ☐ | Security contact (incidents, monitoring) | | | |
| ☐ | Owner of each hand-off between the teams holding these roles | | | |

## B. Documents that must exist

| ☐ | Document | Owner | Minimum content | Where |
|---|---|---|---|---|
| ☐ | **Enterprise policy** (`enterprise-policy`) (P: draft) | Risk & Control + Portfolio Owner | Prohibitions, obligations, permissions typed O/P/F; version 1 approved | |
| ☐ | **Substrate binding** (`builder/substrate-binding.md`) | Platform Operator | Every row filled | repo |
| ☐ | **Substrate operations skill** (`skills/substrate-operations.md`) | Platform Operator | Every row filled; known failure modes listed | repo |
| ☐ | **Demonstration log** (`demonstration-log`) | Platform Operator | R1–R21 (or the team's version): test run, date, evidence, result; what is not yet shown and the team's decision | |
| ☐ | **Price table** | Platform Operator | Price per input and output token per model in use; currency; date; who updates it | |
| ☐ | **Model tier defaults** | Platform Operator + Framework Architect | Tier, model, fallback and effort per role; override procedure | |
| ☐ | **Budget defaults** | Platform Operator + Portfolio Owner | Default caps per level (session per role, item, chain, period); spend that needs portfolio approval | |
| ☐ | **Retention schedule** | Data protection + Risk & Control | Floors per record class (ledger, telemetry, effect traces, raw corpus); archive and deletion | |
| ☐ | **Data classification rules for raw corpus** | Data protection | Which mailboxes, transcripts and libraries a Distiller may read; labels; what the ingestion gateway masks | |
| ☐ | **Disclosure wording** | Risk & Control + legal | The line agent-generated external messages carry; the explanation-artefact template for adverse decisions | |
| ☐ | **Workers' information pack** | HR + legal | What staff and their representatives are told before an instance runs at their workplace | |
| ☐ | **DPIA / FRIA template and trigger** | Data protection + legal | When an instance needs one, and the template the Builder links | |
| ☐ | **Agent identity runbook** | Platform Operator | Provisioning per instance, per-session tokens, registration, review, revocation on retirement | |
| ☐ | **Containment runbook** | Platform Operator + security | The four steps (freeze, prepare-only, pause, quarantine): who triggers, how, how lifted, who is notified | |
| ☐ | **Incident runbook** | Platform Operator + security + legal | Classes, register, suspension, internal escalation, external reporting duties and deadlines | |
| ☐ | **Release procedure** | Framework Architect | As in the README; who deploys a release to the platform; how instances are notified | |
| ☐ | **Regression bank** (P: examples only) | Framework Architect | Golden cases from the two examples, with expected facts per role; how to run it | |
| ☐ | **Review calendars** (P: pilot end review only) | Framework Owner + Portfolio Owner | Framework review and portfolio review: cadence and first dates booked | |

## C. Platform demonstrated (summary of the demonstration log)

| ☐ | Group | Requirements | Key test |
|---|---|---|---|
| ☐ | **Measurement first** (P: R17 single cap; R8 never deferred) | R8, R17 | A test session's tokens, spans and outcome land where the Auditor reads; cost derived; a small item budget exhausted pauses new arms |
| ☐ | **Engine and people** (P: R3 subset for the pilot's flows) | R3, R19 | The failure classes of `docs/why.md` pass; a human turn escalates deputy → superior on SLA |
| ☐ | **Work and change** | R1, R2, R4, R5, R6 | Typed item created; facts visible on the item; propose → promote → roll back; delta computed and reconciled; a red check blocks promotion |
| ☐ | **Classifier** (P) | R7 | Question bank calibrated on a labelled sample — or degradation accepted and budgets recomputed |
| ☐ | **Runtime and identity** | R9, R10 | Model fallback engages; an agent's attempt to write an approval or edit a budget is refused; a tool call outside policy is refused and logged |
| ☐ | **Knowledge** | R11, R12, R13 | In-place edit of a decision refused; cross-layer write refused; an Executor cannot read a mailbox |
| ☐ | **Control plane** (P: R16 manual monitoring) | R14, R15, R16, R18 | Proposal cannot be armed without a ruling; approval without scope refused; orchestrator stopped → independent monitor flags it; external effect without approval refused |
| ☐ | **Audit and ingestion** (P: tamper-evidence only; ingestion gateway required) | R20 | Tampered ledger batch detected; embedded instruction in a document masked or flagged |
| ☐ | **Registry** | R21 | Unregistered instance cannot arm; lapsed review degrades to prepare-only; departed owner escalates |

## C2. Framework agents
| ☐ | Item |
|---|---|
| ☐ | Builder and Readiness Agent registered with maturity **pilot**, owner the Framework Owner |
| ☐ | Instantiation limit and exit criteria for each set and signed by the Framework Owner |
| ☐ | Attending Framework Architect named for the Builder's pilot sessions; reviewing Platform Operator named for the Readiness Agent |

## D. Dry run

| ☐ | Step | Evidence |
|---|---|---|
| ☐ | A friendly owner and a small real task chosen | |
| ☐ | Builder session steps 0–7 completed; instance files generated | |
| ☐ | First supervised run with every gate human; ledger read | |
| ☐ | Registry entry active; agents registered | |
| ☐ | Builder ledger closed; corrections filed to the framework queue | |
| ☐ | Regression bank extended with the dry run's cases | |

## Go-live decision

Decided by: ____ date ____ · Profile: pilot / production · Adaptations: see `adaptation-register` · Rows not yet shown and accepted as such: ____

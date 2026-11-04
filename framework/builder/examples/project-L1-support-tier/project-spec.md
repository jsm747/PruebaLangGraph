# Premium support tier — spec

**Entry level:** L1  **Owner:** Head of Customer Success (CS-Head)  **Version:** 1  **Framework version:** 0.1

## Purpose
Decide, with a quantified business case, whether to launch a paid premium support tier (faster SLA, named contact) for existing customers, and if so with which price and scope. The decision at the L1 gate is "invest in planning" or "stop".

## Principles
- P1. Revenue assumptions come from the customer base we have, not from market reports alone.
- P2. Any cost that depends on headcount is modelled with hiring lead time, not as instantaneous.
- P3. Where two assumptions are equally defensible, the business case carries both as a sensitivity, not the optimistic one.

## Boundaries
- Does not design the tier's operations, tooling or contracts (L2+).
- Does not contact customers (that would be an external effect; none in L1).
- Does not touch pricing of existing plans.

## Deliverables
| Deliverable | Canonical representation | Human rendering | Owner at the end |
|---|---|---|---|
| Business case model | spreadsheet (cell-level diff) | same | CS-Head |
| Assumptions register | structured list: id, assumption, value, source anchor, confidence, sensitivity flag | document | CS-Head |
| Risk register | structured list | document | CS-Head |
| L1 memo for the gate | text (extracted, line diff) | document | CS-Head |

## Acceptance criteria (assertable)
- A1. Every assumption in the register has a source anchor or is marked ESTIMATE with its owner.
- A2. The model reproduces, from the register's values alone, the headline numbers in the memo (revenue year 1–3, cost year 1–3, break-even month).
- A3. Sensitivities exist for every assumption flagged critical (at least: attach rate, price, support cost per ticket, hiring lead time).
- A4. The memo states the decision requested and the two alternatives considered (no tier; tier bundled into the top plan).
- A5. The risk register has at least one risk per principle P1–P3.

## Invariants (executable)
| Id | Check | Pre-execution result | Expected at end | Must exist by milestone |
|---|---|---|---|---|
| Inv.1 | model balance: revenue − cost = margin in every year, to the cent | no model | green | M1 |
| Inv.2 | every register row with flag=critical has a sensitivity row | no register | green | M2 |
| Inv.3 | memo headline numbers == model outputs (cell references) | no memo | green | M3 |

## Existing state this project relies on
- `state: 1,240 active customer accounts as of 2026-09-30 ⇐ CRM export 2026-10-01, information map #3`
- `state: average tickets per account per month = 2.3 ⇐ support system report Q3-2026, information map #4`
- `UNKNOWN: whether the top plan's contract allows an add-on — Executor verifies in the contract template (information map #2); if not, escalate.`

## Decisions already taken
- DR-001 — the tier is an add-on to existing plans, not a new plan (CS-Head, 2026-10-10).
- DR-002 — price explored in the range 8–15 % of the base plan (CS-Head with CFO, 2026-10-12).

## External effects this project may produce
None at L1.

# #02 — Assumptions register with anchors

**Chain position:** 2 of 5  **Depends on:** 01  **Next:** 03  **Milestone:** M2
**Level:** L1  **Discovery item?** no  **External effect:** none

## Purpose
Produce the assumptions register the model consumes: every input of the model as a row with value, source anchor, confidence and critical flag.

## Contract
### Acceptance criteria
- A1 (spec A1). Every row has `source` as an anchor into the information map, or `ESTIMATE` with `owner`.
- A2. Every input cell of the model skeleton (item 01) maps to exactly one row.
- A3. Rows for: active accounts, attach rate, price as % of base plan, tickets per account, support cost per ticket, hiring lead time, churn effect — all present.

### Invariants
| Id | Check | Pre-execution result |
|---|---|---|
| Inv.2a | count(rows with flag=critical) ≥ 4 | 0 rows (no register) |
| Inv.2b | every model input cell has a register id | model skeleton has 11 unmapped inputs |

### Anchors to existing material
- `state: 1,240 active accounts ⇐ CRM export 2026-10-01 (info map #3)`
- `state: 2.3 tickets/account/month ⇐ support report Q3-2026 (info map #4)`
- `UNKNOWN: support cost per ticket — no report exists; Executor asks Finance through the process door for the Q3 figure; if unavailable within SLA, ESTIMATE with owner = Controller.`

### Decisions
| Decision | Status |
|---|---|
| price range | derivable from DR-002 ("explored in the range 8–15 % of the base plan") |
| attach rate value | free within 5–25 %, flagged critical |
| churn effect | closed: modelled as zero in L1, listed as a risk (P3) |

### Deliverable
Assumptions register, structured list, in `/business-case/assumptions.xlsx` sheet `register`.

### Scope declaration structure
Sheet `register` rows by id; sheet `model` input cells only (column C).

## Critique
`critique:lgtm` by Critic on 2026-10-22.

## Execution (filled by the Executor)
**Scope declared:** register rows R01–R07; model!C4:C14
**Polarity:** complete
**Decisions derived:** price range ⇐ "explored in the range 8–15 % of the base plan" (DR-002, D1)
**Blocked on:** —

## Verification
`delta:computed` · `scope:match` · `checks:green` · classifier: A1 0.97 → `criteria:met`, A3 0.99 → `criteria:met` · `review:pass` (A2 verified by hand: 11/11 inputs mapped)

## Closure
`integrated` 2026-10-27 by Integrator · next: #03 armed.

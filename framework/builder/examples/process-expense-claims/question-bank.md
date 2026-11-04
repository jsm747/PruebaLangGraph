# Questions — Expense claims v1

## Risk score
State: the case data, the proposal, policy §2–4 as text. Scale 0–1: likelihood that an approver would decide differently from the proposal. Bands: low < 0.30 ≤ medium < 0.60 ≤ high.

## Assertions
| Id | Criterion | Type | State | Threshold | Grey | Fact | On fail | On grey |
|---|---|---|---|---|---|---|---|---|
| Q-A1 | every reimbursed line's receipt matches its amount and date | boolean | line + receipt OCR text | 0.95 | 0.80–0.95 | `criteria:A1` | human | review |
| Q-A3 | each rejection cites the right rule for the facts | boolean | line + rule text | 0.95 | 0.80–0.95 | `criteria:A3` | human | review |
| Q-R5 | the attendees named are plausibly external (client) | boolean | attendees + purpose | 0.90 | 0.75–0.90 | `criteria:R5` | human | human |
| Q-H5 | the purpose text names a customer or a gift | boolean | purpose text | 0.70 | — | `rule:H5` | — | — |

A2, A4, A5 are deterministic checks, not questions.

## Calibration (October 2026, first month)
| Id | Band | Observed | n | By group (cost centre) | Drift |
|---|---|---|---|---|---|
| Q-A1 | ≥ 0.95 | 0.97 | 412 | none > 0.02 | keep |
| Q-H5 | ≥ 0.70 | 0.61 | 88 | CC-410 0.48 | retune: too many false H5 routes in sales (customer names in trip refs) |
